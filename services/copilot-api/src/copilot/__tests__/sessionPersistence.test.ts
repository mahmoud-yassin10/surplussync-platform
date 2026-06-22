import { beforeEach, describe, expect, it } from "vitest";
import request from "supertest";
import { createLabApp } from "../../server/createApp";
import { UserRole } from "../../types";
import { buildCanonicalForecastFallback, buildCanonicalWhatIfTripCancelledFallback } from "../canonicalMlFeatures";
import { CORRECTED_ATTENDANCE } from "../demoConstants";
import {
  clearAllSessions,
  PersistedLabSession,
  removeSessionFromMemoryForTest,
} from "../sessionStore";
import { SessionPersistence } from "../sessionPersistence";

const TEST_TOKEN = "test-main-app-token";

class FakePersistence implements SessionPersistence {
  mode: "memory" | "redis";
  store = new Map<string, PersistedLabSession>();

  constructor(mode: "memory" | "redis" = "redis") {
    this.mode = mode;
  }

  async load(sessionId: string) {
    return this.store.get(sessionId) ?? null;
  }

  async save(session: PersistedLabSession) {
    this.store.set(session.sessionId, structuredClone(session));
  }

  async delete(sessionId: string) {
    this.store.delete(sessionId);
  }
}

function mockMlFetch() {
  return async (url: string) => {
    if (url.endsWith("/v1/what-if")) {
      return new Response(JSON.stringify(buildCanonicalWhatIfTripCancelledFallback()), {
        headers: { "content-type": "application/json" },
      });
    }
    return new Response(JSON.stringify(buildCanonicalForecastFallback()), {
      headers: { "content-type": "application/json" },
    });
  };
}

function createApp(persistence?: SessionPersistence) {
  return createLabApp({
    geminiAvailable: false,
    mainAppServiceToken: TEST_TOKEN,
    mlFetchFn: mockMlFetch(),
    sessionPersistence: persistence,
  });
}

function auth() {
  return { Authorization: `Bearer ${TEST_TOKEN}` };
}

function baselinePayload(proposalsPermitted = true) {
  return {
    source: "surplussync-plus",
    stateVersion: "ssp_state_v2",
    role: UserRole.CAFETERIA_MANAGER,
    operational: {
      expectedAttendance: 528,
      recommendedPreparation: 562,
      currentPreparationPlan: 730,
      attendanceCorrected: false,
      provisionalAlertsSent: false,
      selectedPartnerId: "metro-food-bank",
      proposalsPermitted,
    },
  };
}

describe("session persistence and health", () => {
  beforeEach(() => clearAllSessions());

  it("reports memory persistence when Redis is not configured", async () => {
    const res = await request(createApp()).get("/health");
    expect(res.status).toBe(200);
    expect(res.body.sessionPersistence).toBe("memory");
    expect(res.body).not.toHaveProperty("token");
  });

  it("reports injected durable persistence mode", async () => {
    const res = await request(createApp(new FakePersistence("redis"))).get("/health");
    expect(res.body.sessionPersistence).toBe("redis");
    expect(res.body.geminiAvailable).toBe(false);
  });

  it("creates, persists, evicts from memory, and rehydrates a session", async () => {
    const persistence = new FakePersistence();
    const app = createApp(persistence);
    const created = await request(app).post("/api/session").send({});
    const sessionId = created.body.sessionId as string;
    expect(persistence.store.has(sessionId)).toBe(true);

    removeSessionFromMemoryForTest(sessionId);
    const state = await request(app).get(`/api/session/${sessionId}/state`);
    expect(state.status).toBe(200);
    expect(state.body.state.sessionId).toBe(sessionId);
  });

  it("keeps an approved proposal executed after rehydration", async () => {
    const persistence = new FakePersistence();
    const app = createApp(persistence);
    const created = await request(app).post("/api/session").send({ role: UserRole.SCHOOL_ADMINISTRATOR });
    const sessionId = created.body.sessionId as string;
    const turn = await request(app)
      .post("/api/copilot")
      .send({ sessionId, message: "change attendance trip cancelled" });
    const proposalId = turn.body.state.proposals[0].proposalId;
    await request(app).post(`/api/session/${sessionId}/proposals/${proposalId}/approve`);

    removeSessionFromMemoryForTest(sessionId);
    const state = await request(app).get(`/api/session/${sessionId}/state`);
    expect(state.body.state.forecast.expectedAttendance).toBe(CORRECTED_ATTENDANCE);
    expect(state.body.state.proposals[0].status).toBe("EXECUTED");
  });

  it("keeps manual mode enforced after rehydration", async () => {
    const persistence = new FakePersistence();
    const app = createApp(persistence);
    const created = await request(app).post("/api/session").send({ role: UserRole.SCHOOL_ADMINISTRATOR });
    const sessionId = created.body.sessionId as string;
    await request(app)
      .post(`/api/integration/session/${sessionId}/reconcile`)
      .set(auth())
      .send(baselinePayload(false));

    removeSessionFromMemoryForTest(sessionId);
    const res = await request(app)
      .post("/api/copilot")
      .send({ sessionId, message: "change attendance trip cancelled" });
    expect(res.body.state.proposalsPermitted).toBe(false);
    expect(res.body.state.proposals).toHaveLength(0);
  });

  it("keeps partner prerequisites enforced after rehydration", async () => {
    const persistence = new FakePersistence();
    const app = createApp(persistence);
    const created = await request(app).post("/api/session").send({ role: UserRole.CAFETERIA_MANAGER });
    const sessionId = created.body.sessionId as string;

    removeSessionFromMemoryForTest(sessionId);
    const res = await request(app)
      .post(`/api/session/${sessionId}/proposals/partner-selection`)
      .send({ partnerId: "harbor-shelter" });
    expect(res.status).toBe(403);
    expect(res.body.error).toBe("PARTNER_PREREQUISITES_INCOMPLETE");
  });

  it("deletes persisted state through integration deletion", async () => {
    const persistence = new FakePersistence();
    const app = createApp(persistence);
    const created = await request(app).post("/api/session").send({});
    const sessionId = created.body.sessionId as string;
    expect(persistence.store.has(sessionId)).toBe(true);

    const del = await request(app).delete(`/api/integration/session/${sessionId}`).set(auth());
    expect(del.status).toBe(204);
    expect(persistence.store.has(sessionId)).toBe(false);
  });
});
