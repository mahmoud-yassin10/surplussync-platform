import express, { Express, Request, Response } from "express";
import { GoogleGenAI } from "@google/genai";
import { FunctionCall } from "@google/genai";
import { runCopilotTurn } from "../copilot/geminiRunner";
import { ForecastProvider } from "../copilot/forecastProvider";
import {
  AuditAmendmentRequestSchema,
  CopilotRequestSchema,
  CreateSessionRequestSchema,
  PartnerSelectionRequestSchema,
  UpdateSessionRoleSchema,
} from "../copilot/schemas";
import {
  appendAuditAmendment,
  approveProposal,
  createPartnerSelectionProposal,
  createSession,
  deleteIntegrationSession,
  getKnownPartnerIds,
  getPersistedSession,
  getSessionState,
  hydratePersistedSession,
  rejectProposal,
  updateSessionRole,
} from "../copilot/sessionStore";
import { resolveSessionPersistence, SessionPersistence } from "../copilot/sessionPersistence";
import { authorizeMainAppService } from "../copilot/integrationAuth";
import { reconcileSessionFromMainApp } from "../copilot/reconcileSessionFromMainApp";
import { validateReconciliationRequest } from "../copilot/reconciliationSchemas";
import { UserRole } from "../types";
import type { MlFetchFn } from "../copilot/forecastProvider";

export interface LabAppOptions {
  isProduction?: boolean;
  geminiAvailable?: boolean;
  geminiApiKey?: string;
  port?: number;
  forecastProvider?: ForecastProvider;
  mlFetchFn?: MlFetchFn;
  testGeminiSteps?: Array<{ functionCalls?: FunctionCall[]; text?: string }>;
  /** Server-only integration token override for tests. */
  mainAppServiceToken?: string | null;
  sessionPersistence?: SessionPersistence;
}

function resolveGeminiClient(options: LabAppOptions): GoogleGenAI | null {
  if (options.geminiAvailable === false) return null;
  if (options.geminiAvailable === true) {
    return {
      models: {
        generateContent: async () => ({
          text: JSON.stringify({
            answer: "Controlled tool-loop explanation.",
            answerType: "FACT",
            evidence: [],
            provenance: [{ source: "Test Gemini", status: "DERIVED" }],
            uncertainty: { level: "LOW", explanation: "Test mode." },
            limitations: [],
          }),
          functionCalls: [],
        }),
      },
    } as unknown as GoogleGenAI;
  }
  const API_KEY = options.geminiApiKey ?? process.env.GEMINI_API_KEY;
  if (!API_KEY || API_KEY === "MY_GEMINI_API_KEY" || API_KEY.trim() === "") {
    return null;
  }
  try {
    return new GoogleGenAI({
      apiKey: API_KEY,
      httpOptions: { headers: { "User-Agent": "aistudio-build" } },
    });
  } catch {
    return null;
  }
}

export function createLabApp(options: LabAppOptions = {}): Express {
  const app = express();
  app.use(express.json());

  const isProduction = options.isProduction ?? process.env.NODE_ENV === "production";
  const PORT = options.port ?? 3000;
  const ai = resolveGeminiClient(options);
  const forecastProvider =
    options.forecastProvider ??
    new ForecastProvider({
      fetchFn: options.mlFetchFn,
    });
  const integrationToken =
    options.mainAppServiceToken !== undefined
      ? options.mainAppServiceToken
      : process.env.MAIN_APP_SERVICE_TOKEN ?? null;
  const sessionPersistence = options.sessionPersistence ?? resolveSessionPersistence();

  async function hydrateSession(sessionId: string): Promise<void> {
    if (getSessionState(sessionId)) return;
    const persisted = await sessionPersistence.load(sessionId);
    if (persisted) hydratePersistedSession(persisted);
  }

  async function persistSession(sessionId: string): Promise<void> {
    const session = getPersistedSession(sessionId);
    if (session) await sessionPersistence.save(session);
  }

  async function deleteSession(sessionId: string): Promise<boolean> {
    const deleted = deleteIntegrationSession(sessionId);
    await sessionPersistence.delete(sessionId);
    return deleted;
  }

  function requireMainAppAuth(req: Request, res: Response): boolean {
    const auth = authorizeMainAppService(req.get("authorization"), integrationToken);
    if (auth.ok === false) {
      res.status(auth.statusCode).json({ error: auth.error });
      return false;
    }
    return true;
  }

  app.get("/health", (_req: Request, res: Response) => {
    res.status(200).json({
      status: "ok",
      service: "surplussync-copilot-api",
      geminiAvailable: !!ai,
      forecastSourceConfigured: !!process.env.ML_SERVICE_URL?.trim(),
      sessionPersistence: sessionPersistence.mode,
    });
  });

  app.post("/api/integration/session/:sessionId/reconcile", async (req: Request, res: Response) => {
    if (!requireMainAppAuth(req, res)) return;
    await hydrateSession(req.params.sessionId);

    const validation = validateReconciliationRequest(
      req.body,
      getKnownPartnerIds(req.params.sessionId)
    );
    if (validation.ok === false) {
      res.status(validation.statusCode).json({ error: validation.error });
      return;
    }

    const result = reconcileSessionFromMainApp(req.params.sessionId, validation.data);
    if (!result.ok) {
      res.status(result.statusCode).json({ error: result.error });
      return;
    }

    res.status(200).json({
      state: result.state,
      changed: result.changed,
      idempotent: result.idempotent,
    });
    await persistSession(req.params.sessionId);
  });

  app.delete("/api/integration/session/:sessionId", async (req: Request, res: Response) => {
    if (!requireMainAppAuth(req, res)) return;

    await hydrateSession(req.params.sessionId);
    const deleted = await deleteSession(req.params.sessionId);
    if (!deleted) {
      res.status(404).json({ error: "Session not found" });
      return;
    }

    res.status(204).send();
  });

  app.post("/api/session", async (req: Request, res: Response) => {
    const parsed = CreateSessionRequestSchema.safeParse(req.body ?? {});
    if (!parsed.success) {
      res.status(400).json({ error: "Invalid session creation payload" });
      return;
    }
    const role = (parsed.data.role as UserRole) ?? UserRole.CAFETERIA_MANAGER;
    const state = createSession(role);
    res.status(201).json({
      sessionId: state.sessionId,
      state,
      notice: "Demo session isolation only — not production authentication.",
    });
    await persistSession(state.sessionId);
  });

  app.get("/api/session/:sessionId/state", async (req: Request, res: Response) => {
    await hydrateSession(req.params.sessionId);
    const state = getSessionState(req.params.sessionId);
    if (!state) {
      res.status(404).json({ error: "Session not found" });
      return;
    }
    res.json({ state });
  });

  app.patch("/api/session/:sessionId/role", async (req: Request, res: Response) => {
    const parsed = UpdateSessionRoleSchema.safeParse(req.body);
    if (!parsed.success) {
      res.status(400).json({ error: "Invalid role payload" });
      return;
    }
    await hydrateSession(req.params.sessionId);
    const state = updateSessionRole(req.params.sessionId, parsed.data.role as UserRole);
    if (!state) {
      res.status(404).json({ error: "Session not found" });
      return;
    }
    res.json({ state });
    await persistSession(req.params.sessionId);
  });

  app.post("/api/session/:sessionId/audit/amendment", async (req: Request, res: Response) => {
    const parsed = AuditAmendmentRequestSchema.safeParse(req.body);
    if (!parsed.success) {
      res.status(400).json({ error: "Invalid audit amendment payload" });
      return;
    }
    await hydrateSession(req.params.sessionId);
    const result = appendAuditAmendment(
      req.params.sessionId,
      parsed.data.reason,
      parsed.data.relatedAuditId
    );
    if (!result.ok) {
      res.status(result.statusCode).json({ error: result.error });
      return;
    }
    res.status(201).json({ state: result.state, amendment: result.amendment });
    await persistSession(req.params.sessionId);
  });

  app.post("/api/session/:sessionId/proposals/partner-selection", async (req: Request, res: Response) => {
    const parsed = PartnerSelectionRequestSchema.safeParse(req.body);
    if (!parsed.success) {
      res.status(400).json({ error: "Invalid partner selection payload" });
      return;
    }
    await hydrateSession(req.params.sessionId);
    const result = createPartnerSelectionProposal(req.params.sessionId, parsed.data.partnerId);
    if (!result.ok) {
      res.status(result.statusCode).json({ error: result.error });
      return;
    }
    res.status(result.statusCode).json({ state: result.state, proposals: result.proposals });
    await persistSession(req.params.sessionId);
  });

  app.post("/api/session/:sessionId/proposals/:proposalId/approve", async (req: Request, res: Response) => {
    await hydrateSession(req.params.sessionId);
    const result = approveProposal(req.params.sessionId, req.params.proposalId);
    if (!result.ok) {
      res.status(result.statusCode).json({ error: result.error });
      return;
    }
    res.json({ state: result.state });
    await persistSession(req.params.sessionId);
  });

  app.post("/api/session/:sessionId/proposals/:proposalId/reject", async (req: Request, res: Response) => {
    await hydrateSession(req.params.sessionId);
    const result = rejectProposal(req.params.sessionId, req.params.proposalId);
    if (!result.ok) {
      res.status(result.statusCode).json({ error: result.error });
      return;
    }
    res.json({ state: result.state });
    await persistSession(req.params.sessionId);
  });

  app.post("/api/copilot", async (req: Request, res: Response) => {
    try {
      const parsed = CopilotRequestSchema.safeParse(req.body);
      if (!parsed.success) {
        res.status(400).json({ error: "Invalid copilot request", details: parsed.error.flatten() });
        return;
      }

      const { sessionId, message } = parsed.data;
      await hydrateSession(sessionId);
      const session = getSessionState(sessionId);
      if (!session) {
        res.status(404).json({ error: "Session not found" });
        return;
      }

      const forceMockRequested = parsed.data.forceMockMode === true;
      const forceMockMode = !isProduction && forceMockRequested;
      const useMock = forceMockMode || !ai;

      const turn = await runCopilotTurn({
        sessionId,
        message,
        mode: useMock ? "mock" : "live",
        ai,
        forecastProvider,
        testGeminiSteps: options.testGeminiSteps,
      });

      if (!turn.ok || !turn.processed || "error" in turn.processed) {
        res.status(422).json({ error: turn.error ?? turn.processed?.error ?? "Copilot turn failed" });
        return;
      }

      const apiMode = useMock ? "MOCK_FALLBACK" : "GEMINI_LIVE";
      res.json({
        result: turn.processed.response,
        state: getSessionState(sessionId),
        mode: apiMode,
        runnerMode: turn.mode,
        rejectedProposals: turn.processed.rejectedProposals,
        warning: turn.warning,
      });
      await persistSession(sessionId);
    } catch (error: unknown) {
      console.error("Copilot execution failed:", error);
      const sessionId = req.body?.sessionId;
      if (typeof sessionId !== "string" || !getSessionState(sessionId)) {
        res.status(500).json({ error: "Copilot failed and session is unavailable for fallback" });
        return;
      }
      const fallback = await runCopilotTurn({
        sessionId,
        message: req.body.message ?? "",
        mode: "mock",
        forecastProvider,
      });
      if (!fallback.ok || !fallback.processed || "error" in fallback.processed) {
        res.status(500).json({ error: fallback.error ?? "Copilot fallback failed" });
        return;
      }
      res.json({
        result: fallback.processed.response,
        state: getSessionState(sessionId),
        mode: "MOCK_FALLBACK",
        runnerMode: fallback.mode,
        warning: "Server error encountered. Safely resolved via deterministic tool-loop fallback.",
        rejectedProposals: fallback.processed.rejectedProposals,
      });
      if (typeof sessionId === "string") await persistSession(sessionId);
    }
  });

  app.get("/api/config", (_req: Request, res: Response) => {
    const API_KEY = options.geminiApiKey ?? process.env.GEMINI_API_KEY;
    res.json({
      hasGeminiApiKey: !!API_KEY && API_KEY !== "MY_GEMINI_API_KEY" && API_KEY.trim() !== "",
      activePort: PORT,
      isProduction,
      allowForceMock: !isProduction,
      sessionNotice: "Demo session isolation only — not production authentication.",
      sessionPersistence: sessionPersistence.mode,
    });
  });

  return app;
}
