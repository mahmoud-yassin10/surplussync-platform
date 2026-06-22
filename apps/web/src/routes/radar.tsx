import { createFileRoute } from "@tanstack/react-router";
import { Page, Section } from "../components/shell/AppShell";
import { SurplusRadar } from "../components/forecast/SurplusRadar";
import { HorizonRibbon } from "../components/forecast/HorizonRibbon";

export const Route = createFileRoute("/radar")({
  head: () => ({ meta: [{ title: "Surplus Radar - SurplusSync Plus" }] }),
  component: Radar,
});

function Radar() {
  return (
    <Page kicker="Surplus radar" title="Forecast horizon - 10 school days">
      <div className="grid xl:grid-cols-[minmax(560px,1fr)_minmax(420px,0.82fr)] gap-5 items-start">
        <Section
          title="Risk by horizon ring"
          hint="Pulsing markers indicate high-risk events; outer ring shows partner capacity"
        >
          <SurplusRadar />
        </Section>

        <div className="space-y-5">
          <Section title="Day-by-day ribbon">
            <HorizonRibbon variant="compact" />
          </Section>

          <Section title="How to read the radar" padded>
            <div className="grid sm:grid-cols-3 gap-3 text-[11.5px] text-[var(--color-text-soft)]">
              <div>
                <div className="font-medium text-[var(--color-text)] mb-0.5">Ring distance</div>
                Inner marks are near-term school days; outer marks are later horizon days.
              </div>
              <div>
                <div className="font-medium text-[var(--color-text)] mb-0.5">Marker color</div>
                Red means high surplus risk, amber means moderate, green means low.
              </div>
              <div>
                <div className="font-medium text-[var(--color-text)] mb-0.5">Capacity lines</div>
                Dashed green spokes show recovery partners that can reserve meals.
              </div>
            </div>
          </Section>
        </div>
      </div>
    </Page>
  );
}
