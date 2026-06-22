import { describe, expect, it } from "vitest";
import {
  DEMO_FOCUS_DATE,
  formatFocusDateLong,
  formatFocusDateShort,
  formatFocusDateSlash,
  isFocusDateMonday,
} from "../demo-date";

describe("demo-date", () => {
  it("anchors focus day to Monday June 22, 2026", () => {
    expect(DEMO_FOCUS_DATE).toBe("2026-06-22");
    expect(isFocusDateMonday()).toBe(true);
    expect(formatFocusDateLong()).toBe("Monday Jun 22, 2026");
    expect(formatFocusDateShort()).toBe("Mon Jun 22");
    expect(formatFocusDateSlash()).toBe("06/22");
  });
});
