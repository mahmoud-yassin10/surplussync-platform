import { Redis } from "@upstash/redis";
import type { PersistedLabSession } from "./sessionStore.js";

export type SessionPersistenceMode = "memory" | "redis";

export interface SessionPersistence {
  mode: SessionPersistenceMode;
  load(sessionId: string): Promise<PersistedLabSession | null>;
  save(session: PersistedLabSession): Promise<void>;
  delete(sessionId: string): Promise<void>;
}

export const memorySessionPersistence: SessionPersistence = {
  mode: "memory",
  async load() {
    return null;
  },
  async save() {
    return;
  },
  async delete() {
    return;
  },
};

function sessionKey(sessionId: string): string {
  return `surplussync:copilot:session:${sessionId}`;
}

function sessionTtlSeconds(): number {
  const raw = process.env.COPILOT_SESSION_TTL_SECONDS;
  const parsed = raw ? Number.parseInt(raw, 10) : 86_400;
  return Number.isFinite(parsed) && parsed > 0 ? parsed : 86_400;
}

export function resolveSessionPersistence(): SessionPersistence {
  const url = process.env.UPSTASH_REDIS_REST_URL?.trim();
  const token = process.env.UPSTASH_REDIS_REST_TOKEN?.trim();
  if (!url || !token) return memorySessionPersistence;

  const redis = new Redis({ url, token });
  return {
    mode: "redis",
    async load(sessionId: string) {
      return redis.get<PersistedLabSession>(sessionKey(sessionId));
    },
    async save(session: PersistedLabSession) {
      await redis.set(sessionKey(session.sessionId), session, { ex: sessionTtlSeconds() });
    },
    async delete(sessionId: string) {
      await redis.del(sessionKey(sessionId));
    },
  };
}
