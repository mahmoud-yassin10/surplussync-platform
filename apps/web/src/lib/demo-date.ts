/** Canonical demonstration timeline, Monday June 22, 2026 focus day. */
export const DEMO_FOCUS_DATE = "2026-06-22";
export const DEMO_TODAY = "2026-06-22";

const DEMO_CLOCK_ANCHOR = `${DEMO_FOCUS_DATE}T12:00:00.000Z`;

export function formatFocusDateLong(): string {
  return "Monday Jun 22, 2026";
}

export function formatFocusDateShort(): string {
  return "Mon Jun 22";
}

export function formatFocusDateSlash(): string {
  return "06/22";
}

/** Demo-anchored ISO timestamp (defaults to noon on focus day). */
export function demoTimestamp(offsetMs = 0): string {
  return new Date(new Date(DEMO_CLOCK_ANCHOR).getTime() + offsetMs).toISOString();
}

export function isFocusDateMonday(): boolean {
  return new Date(`${DEMO_FOCUS_DATE}T12:00:00Z`).getUTCDay() === 1;
}
