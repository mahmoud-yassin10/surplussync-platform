import { createFileRoute } from "@tanstack/react-router";
import { EvidencePage } from "../components/forecast/EvidenceDrawer";

export const Route = createFileRoute("/evidence")({
  head: () => ({ meta: [{ title: "AI Evidence - SurplusSync Plus" }] }),
  component: EvidencePage,
});
