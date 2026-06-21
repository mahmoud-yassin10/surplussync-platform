# Architecture

## System Context

SurplusSync Plus has three services: a TanStack Start web app, a secured AI assistant proposal service, and a FastAPI ML service.

```mermaid
flowchart TB
    User["Authorized cafeteria or admin user"] --> Web["Web app"]
    Web --> ForecastGateway["Forecast gateway"]
    Web --> AssistantGateway["AI assistant gateway"]
    ForecastGateway --> ML["ML service"]
    AssistantGateway --> Assistant["Proposal engine"]
    Assistant --> ML
    Assistant --> Store["Session, proposal, approval, audit state"]
```

## Browser and Server Boundary

The browser never receives the Copilot service token, direct service credentials, or Gemini key. Browser requests go to same-origin frontend routes. The frontend server proxies forecast and assistant requests to private services.

## Forecast Flow

```mermaid
sequenceDiagram
    participant U as User
    participant W as Web
    participant FG as Forecast gateway
    participant ML as ML service
    U->>W: Open forecast
    W->>FG: Request canonical forecast
    FG->>ML: POST /v1/forecast
    ML-->>FG: Point, q10, q90, recommendation
    FG-->>W: Canonical view model
```

## AI Assistant Proposal Flow

```mermaid
sequenceDiagram
    participant U as User
    participant W as Web
    participant A as Assistant API
    participant ML as ML service
    U->>W: Ask operational question
    W->>A: Message with session and role
    A->>ML: Read forecast or simulate if needed
    A-->>W: Explanation and optional pending proposal
    U->>W: Approve proposal
    W->>A: Approval endpoint
    A-->>W: Revalidated approved action
```

## Approval Flow

Every consequential action goes through a human approval gate. The assistant may create pending proposals, but it cannot approve itself or execute irreversible actions.

## Partner Prerequisite Flow

Partner execution is checked against surplus confirmation, checklist completion, recovery window, eligibility, capacity where represented, role, proposal freshness, and operating mode.

## Manual Mode

Assisted mode permits explanations, simulations, and pending proposals. Strict manual mode permits explanations and simulations but blocks executable proposals and approval execution.

## Fallback Behavior

ML fallback is disclosed when the live service is unavailable for the canonical fixture. Gemini is optional; without it the assistant uses deterministic language generation while still retrieving forecast data through the ML pathway when available.

## Audit Behavior

Operational events are append-only in the prototype store. Reset restores demo state; it does not represent production audit retention.
