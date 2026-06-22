import { Link } from "@tanstack/react-router";
import { ArrowDown, ArrowUp, BookOpen, Database, History } from "lucide-react";
import { Page, Section } from "../shell/AppShell";
import { useStore } from "../../lib/store";
import { formatFocusDateShort } from "../../lib/demo-date";

export function EvidenceTrigger({ className = "" }: { className?: string }) {
  return (
    <Link
      to="/evidence"
      className={`text-[12px] px-3 py-1.5 rounded-md border border-[var(--color-line)] hover:bg-[var(--color-surface-2)] flex items-center gap-1.5 ${className}`}
    >
      <BookOpen size={12} /> Why this prediction?
    </Link>
  );
}

export function EvidencePage() {
  const { state } = useStore();
  const f = state.forecast;
  const maxMag = Math.max(1, ...f.influences.map((i) => i.magnitude));

  return (
    <Page
      kicker="AI evidence"
      title={`Why ${formatFocusDateShort()} is predicted at ${f.expectedAttendance} students`}
      actions={
        <Link
          to="/forecast"
          className="text-[12px] px-3 py-1.5 rounded-md border border-[var(--color-line)] hover:bg-[var(--color-surface-2)]"
        >
          Back to forecast
        </Link>
      }
    >
      <div className="grid xl:grid-cols-[minmax(0,1.35fr)_minmax(320px,0.75fr)] gap-5 items-start">
        <div className="space-y-5">
          <Section
            title="Forecast summary"
            hint="Influential inputs, not causes. Ordered by historical correlation magnitude."
          >
            <div className="p-4 grid sm:grid-cols-3 gap-3">
              <Stat label="Expected" value={`${f.expectedAttendance}`} sub="students" />
              <Stat label="80% interval" value={`${f.intervalLow}-${f.intervalHigh}`} sub="students" />
              <Stat label="Data quality" value="High" sub="3 of 3 sources" />
            </div>
          </Section>

          <Section title="Influential inputs">
            <ul className="divide-y divide-[var(--color-line)]">
              {f.influences.map((inf) => (
                <li
                  key={inf.factor}
                  className="grid grid-cols-[22px_1fr_auto] gap-3 px-4 py-3 items-start"
                >
                  {inf.direction === "down" ? (
                    <ArrowDown size={15} className="text-[var(--color-critical)] mt-0.5" />
                  ) : (
                    <ArrowUp size={15} className="text-[var(--color-success)] mt-0.5" />
                  )}
                  <div className="min-w-0">
                    <div className="text-[13px] font-medium text-[var(--color-text)]">
                      {inf.factor}
                    </div>
                    <div className="text-[11.5px] text-[var(--color-text-faint)] mt-0.5">
                      {inf.note}
                    </div>
                    <div className="mt-2 h-1.5 rounded-full bg-[var(--color-line)] overflow-hidden">
                      <div
                        className="h-1.5 rounded-full"
                        style={{
                          width: `${(inf.magnitude / maxMag) * 100}%`,
                          background:
                            inf.direction === "down"
                              ? "var(--color-critical)"
                              : "var(--color-success)",
                        }}
                      />
                    </div>
                  </div>
                  <span className="text-[12px] tnum text-[var(--color-text-soft)] mt-0.5">
                    {inf.direction === "down" ? "-" : "+"}
                    {inf.magnitude}
                  </span>
                </li>
              ))}
            </ul>
          </Section>
        </div>

        <div className="space-y-5">
          <Section
            title="Similar historical days"
            right={<History size={13} className="text-[var(--color-text-faint)]" />}
          >
            <table className="w-full text-[12px]">
              <tbody>
                {f.similarDays.map((d) => (
                  <tr key={d.date} className="border-b border-[var(--color-line)] last:border-0">
                    <td className="px-4 py-2.5 text-[var(--color-text-soft)] tnum">{d.date}</td>
                    <td className="px-4 py-2.5 text-right tnum font-medium">{d.attendance}</td>
                    <td className="px-4 py-2.5 pl-2 text-[var(--color-text-faint)]">{d.note}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </Section>

          <Section
            title="Provenance"
            right={<Database size={13} className="text-[var(--color-text-faint)]" />}
            padded
          >
            <ul className="text-[11.5px] text-[var(--color-text-soft)] space-y-2">
              <li>District attendance system, updated 06:00 daily</li>
              <li>School calendar feed, synced 04:00 daily</li>
              <li>NWS weather API, forecast retrieved 05:30</li>
              <li>Menu participation history, last 180 service days</li>
            </ul>
          </Section>

          <Section title="Limitations" padded>
            <p className="text-[12px] text-[var(--color-text-soft)] leading-relaxed">
              The model cannot anticipate unannounced events, such as last-minute cancellations. It
              does not certify food safety. Estimates carry an 80% interval, and actual attendance
              can fall outside it. Human review is required before consequential action.
            </p>
            <div className="mt-3 flex items-center justify-between text-[10.5px] text-[var(--color-text-faint)]">
              <span>Model: {f.modelVersion}</span>
              <button className="hover:text-[var(--color-text-soft)]">Report incorrect output</button>
            </div>
          </Section>
        </div>
      </div>
    </Page>
  );
}

function Stat({ label, value, sub }: { label: string; value: string; sub: string }) {
  return (
    <div className="rounded-md border border-[var(--color-line)] p-3">
      <div className="text-[10px] uppercase tracking-wider text-[var(--color-text-faint)]">
        {label}
      </div>
      <div className="text-[18px] font-semibold tnum mt-0.5">{value}</div>
      <div className="text-[10.5px] text-[var(--color-text-faint)]">{sub}</div>
    </div>
  );
}
