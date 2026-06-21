# SurplusSync Plus — Full Product Specification

**Document type:** Product requirements, technical specification, AI governance plan, build checklist, and definition of done  
**Version:** 1.0  
**Project:** USAII Global AI Hackathon 2026 — High School Track  
**Challenge direction:** Make Climate Action Local and Real  
**Product status:** Planning  
**Primary demonstration geography:** United States  
**Global expansion examples:** Egypt and other countries  
**Qualifier approval code:** `USAII-2026-L7YYDP`

---

## 0. How to Use This Document

This document is the single source of truth for SurplusSync Plus.

Use it to:

1. Decide what the product must do.
2. Divide work among team members.
3. Prevent scope drift.
4. Track implementation progress.
5. Test the final product.
6. Prepare the Devpost description and pitch video.
7. Verify that AI is necessary, transparent, measurable, and responsibly controlled by humans.

### Status markers

- `[ ]` Not started
- `[-]` In progress
- `[x]` Complete
- `MUST` Required for the core product and final demo
- `SHOULD` Important but may be simplified
- `COULD` Optional enhancement

### Final acceptance rule

The product is considered hackathon-ready only when:

- the primary end-to-end demo works without manual database editing;
- the AI produces evaluated forecasts with uncertainty;
- humans can approve, reject, modify, or override every consequential recommendation;
- schools can communicate with recovery partners;
- the map and operational workflow are functional;
- prevented surplus, recoverable surplus, and nonrecoverable waste are tracked separately;
- all model outputs and actions are auditable;
- data provenance and third-party tools are disclosed;
- the project clearly satisfies the official judging criteria.

---

# 1. Product Overview

## 1.1 Product name

**SurplusSync Plus**

## 1.2 One-line description

SurplusSync Plus is an AI-powered school meal forecasting, food-waste prevention, and surplus recovery network connecting schools with verified food banks, shelters, charities, and community kitchens.

## 1.3 Core promise

SurplusSync Plus helps school cafeteria managers answer three questions:

1. **How much food should we prepare?**
2. **How certain is that recommendation, and what could go wrong?**
3. **If safe, unavoidable surplus remains, which verified partner can receive it in time?**

## 1.4 Product thesis

School meal waste is not only a disposal problem. It is a decision and coordination problem.

Schools often prepare meals using averages that do not fully account for:

- examinations;
- field trips;
- sports events;
- early dismissals;
- holidays;
- weather disruptions;
- fasting periods;
- menu popularity;
- changing enrollment;
- unusual attendance patterns.

Existing food-waste systems often measure waste after it occurs. SurplusSync Plus attempts to prevent avoidable surplus before preparation, then coordinates the safe recovery of unavoidable surplus.

## 1.5 Product principles

1. **Prevention before redistribution**
2. **Student meal availability before waste reduction**
3. **Predictions must include uncertainty**
4. **Humans retain final authority**
5. **Every AI recommendation must be explainable and overridable**
6. **Potential surplus is not a promised donation**
7. **Food safety is decided by qualified humans, not the AI**
8. **Synthetic data must be clearly labeled**
9. **Impact must not be double-counted**
10. **The product must still operate in manual mode if AI is unavailable**

---

# 2. Competition Alignment

## 2.1 Judging criteria

The product should be optimized for the official High School Track rubric:

| Criterion | Weight | SurplusSync Plus response |
|---|---:|---|
| Problem Understanding & Context | 30% | Specific cafeteria manager, specific planning window, clear waste and shortage consequences |
| AI Reasoning | 20% | Event-aware forecasting, menu-level prediction, uncertainty estimation, and constrained optimization |
| Solution Design & Architecture | 20% | Clear input → AI → recommendation → human approval → partner workflow |
| Impact & Insight | 20% | Waste prevented, meals protected, safe surplus recovered, cost saved |
| Responsible AI | 10% | Human approval, overrides, uncertainty, provenance, audit logs, manual mode |

## 2.2 Winning narrative

The project should not claim:

> “We invented food-demand forecasting.”

The project should claim:

> “We turned forecasting into a complete, uncertainty-aware operational system that protects meal availability, prevents avoidable overproduction, and safely coordinates unavoidable surplus.”

## 2.3 Why AI is necessary

The system must demonstrate that it performs better than:

- a normal daily average;
- a same-weekday average;
- fixed calendar rules;
- a standard forecasting baseline.

The AI should add value by:

- learning nonlinear combinations of events;
- predicting demand by menu component;
- estimating uncertainty;
- balancing waste against shortage risk;
- adapting to school-specific patterns;
- ranking compatible recovery partners;
- identifying anomalies and low-quality data.

---

# 3. Scope

## 3.1 Core scope

The hackathon product will include:

- a School Portal;
- a Recovery Partner Portal;
- an Administrator Portal;
- an interactive map;
- school calendar management;
- student count and attendance management;
- meal history and waste history;
- an AI Surplus Radar;
- demand forecasts with intervals and risk estimates;
- a preparation optimizer;
- food-bank and shelter matching;
- provisional and confirmed communication workflows;
- in-app messaging;
- pickup tracking;
- an AI Operations Copilot;
- human approval and override controls;
- AI transparency and provenance;
- model evaluation;
- audit logs;
- impact analytics.

## 3.2 Recovery partner types

The system should support:

- food banks;
- shelters;
- community kitchens;
- verified charities;
- religious organizations;
- school district redistribution centers;
- food rescue organizations.

The database entity should use the general term **Recovery Partner**.

## 3.3 Non-goals for the hackathon

The prototype will not claim to provide:

- legal food-safety certification;
- guaranteed live integration with all U.S. schools;
- guaranteed live integration with all food banks;
- nationwide deployment;
- automated purchase-order placement;
- autonomous food donation approval;
- student-level medical or personal profiling;
- payment processing;
- autonomous vehicle dispatch;
- proof of real-world waste reduction without a real pilot;
- exact nationwide impact extrapolation.

---

# 4. Users and Roles

## 4.1 School Cafeteria Manager

### Goals

- forecast meal demand;
- prevent unnecessary preparation;
- avoid shortages;
- understand why a prediction changed;
- communicate with recovery partners;
- confirm actual surplus;
- track pickup.

### Permissions

- view school forecasts;
- update meal plans;
- approve, modify, or reject recommendations;
- confirm actual meal and surplus data;
- communicate with recovery partners;
- send provisional alerts after confirmation;
- select recovery partners;
- override AI recommendations within policy limits.

## 4.2 School Administrator

### Goals

- maintain accurate school, enrollment, and calendar data;
- review corrections and overrides;
- manage users;
- monitor performance.

### Permissions

- edit school profile;
- edit enrollment and meal eligibility counts;
- import and modify calendar events;
- correct attendance history;
- review audit logs;
- approve major data changes;
- configure school safety floors and policies.

## 4.3 Recovery Partner Coordinator

### Goals

- define capacity;
- receive early forecasts;
- reserve tentative capacity;
- accept confirmed donations;
- coordinate pickup;
- record distribution outcome.

### Permissions

- manage organization profile;
- manage food rules and storage capability;
- update capacity calendar;
- accept, partially accept, or decline requests;
- communicate with schools;
- assign pickup;
- close completed recoveries.

## 4.4 Driver or Volunteer

### Permissions

- view assigned pickup;
- update status;
- report delay;
- confirm collection;
- confirm delivery;
- upload proof if enabled.

## 4.5 Platform Administrator

### Goals

- verify institutions;
- protect system integrity;
- monitor AI performance;
- review safety incidents;
- audit impact claims.

### Permissions

- verify schools and partners;
- manage model versions;
- suspend unsafe functionality;
- review incidents and overrides;
- access system-wide audit logs;
- approve policy changes;
- monitor calibration and drift.

## 4.6 Read-only Judge / Demo Viewer

A demo mode should allow judges to explore the product without editing production records.

---

# 5. Core End-to-End Workflow

## 5.1 Forecast and prevention workflow

1. School calendar and historical data are loaded.
2. The model predicts attendance and menu-level demand.
3. The system generates:
   - expected demand;
   - prediction interval;
   - shortage probability;
   - surplus probability;
   - recommended quantity;
   - explanation.
4. The cafeteria manager reviews the recommendation.
5. The manager:
   - approves;
   - modifies;
   - rejects;
   - switches to manual planning.
6. The action is logged.
7. The final plan becomes the preparation target.

## 5.2 Advance recovery planning workflow

1. The Surplus Radar detects a possible future surplus event.
2. The system identifies compatible recovery partners.
3. The AI drafts a **potential surplus alert**.
4. A school human reviews and approves sending.
5. Partners may:
   - tentatively reserve capacity;
   - decline;
   - request details.
6. No donation is promised yet.

## 5.3 Same-day surplus workflow

1. Staff enter actual attendance and meals served.
2. Staff record untouched remaining food.
3. A human completes the recovery eligibility checklist.
4. The system identifies **potentially recoverable surplus**.
5. The AI ranks compatible partners.
6. A human selects a partner.
7. The selected partner confirms capacity and pickup.
8. Pickup is tracked.
9. Final quantity and distribution are recorded.

## 5.4 Feedback workflow

After service:

- actual demand is stored;
- forecast error is calculated;
- overrides are reviewed;
- partner reliability is updated;
- model performance is updated;
- the school receives a daily outcome report.

---

# 6. School Portal Requirements

## 6.1 School Command Center

### MUST show

- school identity and location;
- registered students;
- meal-eligible students;
- expected attendance;
- predicted attendance;
- current preparation plan;
- AI-recommended quantity;
- current risk level;
- upcoming high-risk days;
- current provisional partner responses;
- confirmed pickups;
- monthly impact summary.

### Acceptance criteria

- [ ] Dashboard loads the selected school’s current data.
- [ ] Forecast cards display date, interval, and risk.
- [ ] High-risk events are visible within five seconds.
- [ ] Data provenance labels are available.
- [ ] User can open “Why this prediction?”

## 6.2 School Profile

### Fields

- school name;
- district;
- address;
- coordinates;
- time zone;
- school type;
- grade range;
- total enrollment;
- meal-eligible population;
- cafeteria capacity;
- service days;
- default preparation lead time;
- minimum meal-service floor;
- contact details;
- verification status.

## 6.3 School Calendar

### Event types

- examination;
- field trip;
- sports event;
- holiday;
- early dismissal;
- school closure;
- teacher development;
- graduation;
- assembly;
- religious or fasting period;
- special meal event;
- emergency disruption;
- custom event.

### Event fields

- title;
- event type;
- start and end;
- affected grades;
- expected attendance impact;
- meal timing impact;
- source;
- confidence in manually estimated effect;
- notes;
- created by;
- last modified by.

### Features

- [ ] Month, week, and agenda views
- [ ] Risk overlay
- [ ] Import from CSV or calendar file
- [ ] Manual creation and editing
- [ ] Event cancellation
- [ ] Audit history
- [ ] AI explanation of expected effect

## 6.4 Enrollment and Attendance

### Aggregated fields

- total registered students;
- meal-eligible students;
- normal attendance;
- actual attendance;
- attendance by grade;
- field-trip absences;
- early-dismissal count;
- meal opt-outs;
- known guests;
- data source;
- timestamp.

### Manual correction

Any correction must record:

- old value;
- new value;
- reason;
- user;
- time;
- supporting note;
- whether a forecast rerun was triggered.

### Acceptance criteria

- [ ] Authorized official can correct a value.
- [ ] Change preview shows forecast impact.
- [ ] Explicit approval is required.
- [ ] Forecast reruns after approval.
- [ ] Original value remains visible in history.
- [ ] Undo is available where safe.

## 6.5 Historical Attendance Analytics

### MUST include

- weekday averages;
- event-day averages;
- examination-day behavior;
- weather-related behavior;
- holiday proximity;
- attendance trend;
- unusual-day detection;
- comparison with enrollment;
- data completeness score.

## 6.6 Meal and Menu History

### Daily meal record

- date;
- menu;
- meal category;
- item;
- quantity ordered;
- quantity delivered;
- quantity prepared;
- quantity served;
- quantity consumed or estimated consumed;
- untouched remainder;
- recoverable amount;
- nonrecoverable waste;
- donated amount;
- meal cost;
- preparation time;
- service time;
- holding conditions;
- packaging;
- allergens;
- notes;
- actual attendance.

### Menu categories

- protein;
- carbohydrate;
- vegetables;
- fruit;
- bread;
- dairy;
- drinks;
- snacks;
- packaged meals;
- special dietary meals;
- custom category.

### Historical detail requirements

The system should provide information commonly unavailable in public datasets by allowing authorized school staff to enter or import:

- item-level preparation history;
- item-level consumption;
- item popularity;
- waste reason;
- batch size constraints;
- supplier minimums;
- substitution history;
- unexpected visitors;
- meal service interruption;
- delivery delay;
- quality complaints;
- menu changes;
- staff judgment notes.

These fields should be optional but clearly improve model quality.

## 6.7 Surplus Radar

### Inputs

- calendar;
- attendance history;
- meal history;
- weather;
- menu;
- recent corrections;
- special events;
- partner capacity.

### Outputs

- date;
- risk category;
- expected attendance;
- expected demand by category;
- lower and upper bound;
- current plan;
- recommended plan;
- preventable surplus estimate;
- shortage probability;
- potential recoverable surplus range;
- data quality;
- similar historical days;
- influential inputs.

### Risk categories

- Low
- Moderate
- High
- Critical review required
- Insufficient data

### Acceptance criteria

- [ ] Every risk has an explanation.
- [ ] Every prediction has an interval.
- [ ] Low-data cases are labeled.
- [ ] User can compare current plan with AI plan.
- [ ] User can simulate a different attendance value.
- [ ] User can approve, modify, or reject.

## 6.8 Preparation Planner

### MUST show

- planned meals;
- forecast demand;
- safety buffer;
- maximum safe reduction;
- shortage probability;
- projected waste;
- projected cost;
- menu-level quantities;
- batch constraints;
- human decision.

### Human actions

- approve;
- modify;
- reject;
- save draft;
- switch to manual;
- request second review.

## 6.9 Live Surplus Confirmation

### Required fields

- actual attendance;
- actual served quantity;
- untouched food quantity;
- category;
- preparation time;
- current time;
- packaging status;
- allergen information;
- temperature record if available;
- collection deadline;
- human eligibility confirmation;
- notes.

### System categories

- prevented surplus;
- potentially recoverable surplus;
- confirmed recoverable surplus;
- nonrecoverable waste.

The AI must not declare food legally or medically safe.

---

# 7. Recovery Partner Portal Requirements

## 7.1 Partner Profile

### Fields

- organization name;
- organization type;
- verification status;
- address;
- coordinates;
- contact person;
- service area;
- working hours;
- accepted food categories;
- rejected food categories;
- packaging requirements;
- allergen restrictions;
- maximum daily capacity;
- refrigeration availability;
- hot holding capability;
- vehicle availability;
- pickup radius;
- minimum notice;
- reliability history;
- emergency contact.

## 7.2 Capacity Calendar

### Features

- daily capacity;
- temporary closure;
- vehicle availability;
- refrigeration availability;
- accepted categories by day;
- tentative reservations;
- confirmed pickups.

## 7.3 Potential Surplus Alerts

The alert must state:

- this is a forecast;
- quantity is a range;
- food is not yet confirmed;
- tentative capacity can be reserved;
- the partner may decline without penalty.

### Partner actions

- reserve capacity;
- reserve partial capacity;
- decline;
- request information;
- set a response expiry.

## 7.4 Confirmed Recovery Requests

### MUST include

- confirmed quantity;
- food categories;
- preparation time;
- holding information;
- packaging;
- allergens;
- collection deadline;
- school location;
- contact person;
- human safety confirmation status.

### Partner actions

- accept;
- partially accept;
- reject;
- propose pickup time;
- request clarification.

## 7.5 Pickup Management

### Statuses

- forecast issued;
- capacity reserved;
- surplus confirmed;
- request accepted;
- driver assigned;
- en route;
- arrived;
- collected;
- delivered;
- distributed;
- cancelled;
- failed.

---

# 8. Interactive Map Requirements

## 8.1 Map entities

- schools;
- food banks;
- shelters;
- community kitchens;
- charities;
- surplus-risk events;
- confirmed recovery opportunities;
- active pickup routes.

## 8.2 Layers

- school surplus-risk heatmap;
- recovery capacity;
- storage capability;
- service radius;
- active pickup routes;
- weather overlay if feasible;
- district or county boundaries.

## 8.3 Map interactions

- click school to view risk;
- click partner to view capacity;
- filter by date;
- filter by food category;
- filter by storage capability;
- show ranked matches;
- preview route;
- view estimated pickup time.

## 8.4 Visual quality requirements

- polished transitions;
- readable legend;
- responsive layout;
- fast loading;
- no excessive animation that hides data;
- risk colors must also include labels for accessibility.

---

# 9. Communication System

## 9.1 Communication types

1. AI Operations Copilot
2. School-to-partner messaging
3. Incident and escalation channel
4. System notifications

## 9.2 Human messaging

### Features

- threaded conversations;
- attachments if feasible;
- structured request cards;
- timestamps;
- read status;
- pickup status;
- cancellation;
- archived history;
- role visibility.

## 9.3 Notifications

Possible channels:

- in-app;
- email;
- SMS simulation;
- WhatsApp simulation.

The demo may simulate external messages, but must clearly label simulations.

---

# 10. AI Operations Copilot

## 10.1 Purpose

The Copilot helps users understand data, simulate decisions, prepare actions, and control the platform through safe natural language.

## 10.2 Context available to the Copilot

- current user and role;
- selected school or partner;
- calendar;
- attendance;
- meal history;
- forecasts;
- partner capacity;
- messages;
- pending approvals;
- policy rules;
- model uncertainty;
- recent overrides.

## 10.3 Supported questions

Examples:

- Why is Thursday high risk?
- Which inputs most affected the prediction?
- What happens if attendance is 540?
- Compare this forecast with similar exam days.
- Which partners can accept packaged meals?
- Why is confidence low?
- Show every manual change made today.
- Draft a potential-surplus alert.
- Create a pickup plan.
- Explain the difference between prevented and recoverable surplus.

## 10.4 Action levels

### Level 1 — Read and explain

No confirmation required.

### Level 2 — Draft and prepare

The Copilot creates a draft only.

### Level 3 — Execute after explicit approval

The Copilot must show a preview and require approval.

### Level 4 — Human-only

The Copilot may not execute.

## 10.5 Human-only decisions

- final food-safety eligibility;
- partner verification;
- reduction below school safety floor;
- final emergency exception;
- deletion of audit history;
- model deployment approval;
- institution suspension;
- unresolved incident closure.

## 10.6 Safe action flow

1. Interpret intent.
2. Check permissions.
3. Retrieve relevant records.
4. Generate proposed action.
5. Show exact changes.
6. Show forecast consequences.
7. Show risks.
8. Request approval.
9. Execute after approval.
10. Write audit log.
11. Offer undo when safe.

## 10.7 Copilot action preview

Every preview must show:

- proposed action;
- reason;
- records affected;
- people notified;
- model impact;
- risk;
- reversibility;
- required approval.

---

# 11. Human in the Loop

## 11.1 Mandatory human approvals

| Decision | AI role | Human decision |
|---|---|---|
| Attendance forecast | Predict | Review/correct |
| Meal demand | Predict | Use or reject |
| Preparation quantity | Recommend | Approve/modify/reject |
| Potential alert | Draft | Approve sending |
| Partner match | Rank | Select |
| Recovery eligibility | Organize evidence | Qualified human confirms |
| Pickup | Propose | Both parties confirm |
| Data correction | Detect/suggest | Authorized official approves |
| Model update | Recommend | Admin approves |
| Partner verification | Summarize | Admin verifies |

## 11.2 Override requirements

Every recommendation must allow:

- accept;
- modify;
- reject;
- defer;
- request review;
- switch to manual.

## 11.3 Override record

- AI recommendation;
- human choice;
- reason;
- role;
- timestamp;
- impact;
- optional evidence;
- whether undo is available.

## 11.4 Override feedback

Overrides may inform later evaluation but must not automatically retrain the model without review.

---

# 12. AI Transparency

## 12.1 Prediction transparency panel

Every forecast should show:

- model output;
- expected demand;
- interval;
- shortage probability;
- surplus probability;
- data quality;
- top influential inputs;
- similar historical days;
- model version;
- training date;
- evaluation metrics;
- known limitations;
- whether the input resembles training data.

## 12.2 Data provenance

Each field should be labeled as:

- real public data;
- school-provided data;
- partner-provided data;
- derived feature;
- synthetic operational data;
- model output;
- human override.

## 12.3 Confidence requirements

Do not display decorative confidence.

Use:

- prediction intervals;
- probability estimates;
- calibration results;
- data-quality score;
- out-of-distribution warning;
- similarity to training examples.

## 12.4 Explanation language

Explanations must say:

- “influential input” rather than “cause” unless causality is proven;
- “estimated” rather than “guaranteed”;
- “potential surplus” before actual confirmation;
- “simulated impact” for synthetic evaluations.

---

# 13. Manual Mode, Shutdown, Rollback, and Audit

## 13.1 Manual controls

- AI recommendations on/off;
- manual planning mode;
- pause automated alerts;
- disable a data source;
- reset draft recommendation;
- report incorrect output;
- escalate to administrator.

## 13.2 Version history

Track:

- original data;
- model forecast;
- corrections;
- revised forecast;
- recommendation;
- approval;
- override;
- actual outcome.

## 13.3 Audit requirements

Audit logs must be immutable in the prototype interface.

Log:

- logins;
- data imports;
- edits;
- forecasts;
- model versions;
- approvals;
- overrides;
- messages;
- partner choices;
- pickup status;
- incident actions.

---

# 14. AI and Machine Learning Specification

## 14.1 ML objectives

1. Predict daily attendance.
2. Predict menu-level meal demand.
3. Estimate uncertainty.
4. Recommend preparation quantities.
5. Detect high-surplus-risk days.
6. Rank compatible partners.
7. Detect anomalous or low-quality input data.

## 14.2 Baselines

### Baseline A — Recent average

Average recent comparable days.

### Baseline B — Same weekday

Average demand for the same weekday.

### Baseline C — Fixed calendar rules

Example adjustments for exam, trip, weather, or closure.

### Baseline D — Standard tabular ML

XGBoost, LightGBM, CatBoost, Random Forest, or equivalent.

### SurplusSync Plus model

Must add:

- event interactions;
- menu-level outputs;
- uncertainty;
- shortage-aware optimization;
- school-specific adaptation;
- data-quality warnings.

## 14.3 Features

### School features

- enrollment;
- meal eligibility;
- grade distribution;
- cafeteria capacity;
- school type.

### Time features

- weekday;
- month;
- week number;
- days before holiday;
- days after holiday;
- season.

### Calendar features

- exam;
- trip;
- sports event;
- early dismissal;
- closure;
- fasting period;
- event interaction count;
- affected grades.

### Weather features

- temperature;
- precipitation;
- snowfall if relevant;
- severe weather flag;
- forecast confidence.

### Attendance features

- recent attendance;
- same-weekday attendance;
- trend;
- volatility;
- event-day attendance;
- correction frequency.

### Meal features

- menu item;
- category;
- popularity;
- recent consumption;
- recent waste;
- batch size;
- special dietary quantity;
- meal cost.

### Partner features

- distance;
- capacity;
- food compatibility;
- vehicle availability;
- storage;
- response time;
- reliability.

## 14.4 Training and validation

- time-based split;
- no random leakage across future dates;
- train, validation, and held-out test periods;
- compare against baselines;
- document synthetic generation;
- evaluate multiple school scenarios if possible.

## 14.5 Prediction outputs

- expected attendance;
- expected demand by category;
- lower/upper interval;
- shortage probability;
- surplus probability;
- recommended quantity;
- maximum safe reduction;
- risk level;
- out-of-distribution warning.

## 14.6 Preparation optimizer

The objective should penalize shortages more heavily than overproduction.

Constraints may include:

- minimum service floor;
- batch size;
- menu component minimum;
- cafeteria capacity;
- budget;
- dietary requirement minimum;
- human-configured safety buffer.

## 14.7 Calibration

Evaluate:

- interval coverage;
- reliability of probability estimates;
- overconfidence rate;
- calibration error if feasible.

## 14.8 Model evaluation metrics

### Forecasting

- MAE;
- RMSE;
- MAPE where appropriate;
- weighted error;
- interval coverage;
- interval width.

### Operational

- meals overproduced;
- meals underproduced;
- meal availability;
- high-waste days detected;
- preventable waste;
- cost;
- false surplus alerts;
- food-bank acceptance rate.

### Safety

- underproduction incidents;
- low-confidence recommendations approved;
- override rate;
- false critical alerts;
- calibration failures.

## 14.9 Explainability

Use one or more:

- SHAP values;
- feature importance;
- similar-day retrieval;
- event contribution summary;
- counterfactual simulation.

---

# 15. U.S. Demonstration Data Strategy

## 15.1 Why use a U.S. case study

- stronger public data availability;
- clearer school district calendars;
- accessible weather history;
- public school enrollment;
- visible food-bank networks;
- easier judge verification.

The product remains global.

## 15.2 Real data targets

- public school or district calendar;
- public enrollment;
- district location;
- historical weather;
- holidays;
- publicly listed food banks;
- publicly available meal program information;
- public county or district context.

## 15.3 Synthetic operational data

Likely synthetic:

- daily meals prepared;
- daily meals consumed;
- item-level waste;
- same-day partner capacity;
- detailed pickup outcomes.

## 15.4 Synthetic data rules

- label synthetic fields;
- explain generation assumptions;
- cite assumptions;
- hold out test periods;
- avoid creating unrealistically easy patterns;
- include noise and anomalies;
- do not claim real-world effectiveness.

## 15.5 Data dictionary

The repository must include:

- field name;
- type;
- unit;
- source;
- real/synthetic/derived label;
- allowed range;
- missing-value handling;
- privacy level;
- use in model.

---

# 16. Backend Architecture

## 16.1 Suggested architecture

- frontend web app;
- API backend;
- relational database;
- ML service;
- background job scheduler;
- notification service;
- map/geospatial service;
- file storage;
- audit service.

## 16.2 Suggested implementation options

### Option A

- Next.js
- TypeScript
- PostgreSQL
- Prisma
- FastAPI Python ML service
- Redis or simple job queue
- Mapbox or Leaflet
- WebSockets or polling

### Option B

- React
- Firebase
- Python ML service
- Cloud Functions
- Firestore
- Mapbox or Leaflet

Choose one architecture and avoid mixing unnecessary frameworks.

## 16.3 Service boundaries

- Authentication Service
- School Data Service
- Calendar Service
- Attendance Service
- Meal Service
- Forecasting Service
- Optimization Service
- Partner Service
- Matching Service
- Messaging Service
- Notification Service
- Pickup Service
- AI Copilot Service
- Audit Service
- Admin Service

---

# 17. Database Model

## 17.1 Core entities

```text
User
Role
Permission
School
SchoolOfficial
SchoolCalendarEvent
EnrollmentRecord
AttendanceRecord
MealMenu
MealItem
MealPreparationRecord
MealConsumptionRecord
WasteRecord
Forecast
ForecastRun
ForecastFeature
PredictionInterval
PreparationRecommendation
HumanApproval
HumanOverride
ManualCorrection
RecoveryPartner
PartnerVerification
PartnerCapacity
PartnerFoodRule
PotentialSurplusAlert
ConfirmedSurplus
PartnerMatch
Conversation
Message
AIConversation
AIMessage
AIActionProposal
AIActionExecution
AIExplanation
Pickup
Delivery
ImpactRecord
Incident
Escalation
ModelVersion
DataSource
DataProvenance
DataQualityAssessment
AuditLog
RollbackRecord
```

## 17.2 Key relationships

- School has many events.
- School has many attendance records.
- School has many meal records.
- Forecast belongs to school and date.
- Forecast has one or more menu-level predictions.
- Forecast may produce a recommendation.
- Recommendation may receive approval or override.
- Potential surplus alert may notify multiple partners.
- Confirmed surplus may create multiple ranked matches.
- Pickup belongs to confirmed surplus and partner.
- Every consequential action creates an audit log.

---

# 18. API Requirements

## 18.1 Authentication

- `POST /auth/login`
- `POST /auth/logout`
- `GET /auth/me`

## 18.2 Schools

- `GET /schools`
- `GET /schools/:id`
- `PATCH /schools/:id`
- `GET /schools/:id/dashboard`

## 18.3 Calendar

- `GET /schools/:id/events`
- `POST /schools/:id/events`
- `PATCH /events/:id`
- `DELETE /events/:id` with audit preservation
- `POST /schools/:id/events/import`

## 18.4 Attendance

- `GET /schools/:id/attendance`
- `POST /schools/:id/attendance`
- `PATCH /attendance/:id`
- `POST /attendance/:id/correct`

## 18.5 Meals

- `GET /schools/:id/meals`
- `POST /schools/:id/meals`
- `PATCH /meals/:id`
- `POST /schools/:id/meals/import`

## 18.6 Forecasts

- `POST /schools/:id/forecasts/run`
- `GET /forecasts/:id`
- `GET /schools/:id/forecasts`
- `POST /forecasts/:id/simulate`
- `POST /forecasts/:id/approve`
- `POST /forecasts/:id/override`
- `POST /forecasts/:id/reject`

## 18.7 Partners

- `GET /partners`
- `GET /partners/:id`
- `PATCH /partners/:id`
- `GET /partners/:id/capacity`
- `POST /partners/:id/capacity`

## 18.8 Alerts and recovery

- `POST /surplus-alerts/draft`
- `POST /surplus-alerts/:id/send`
- `POST /surplus-alerts/:id/reserve`
- `POST /confirmed-surplus`
- `GET /confirmed-surplus/:id/matches`
- `POST /confirmed-surplus/:id/select-partner`

## 18.9 Messaging

- `GET /conversations`
- `POST /conversations`
- `POST /conversations/:id/messages`

## 18.10 Copilot

- `POST /copilot/chat`
- `POST /copilot/action-proposals`
- `POST /copilot/action-proposals/:id/approve`
- `POST /copilot/action-proposals/:id/reject`
- `POST /copilot/action-executions/:id/undo`

## 18.11 Audit

- `GET /audit`
- `GET /audit/:entityType/:entityId`

---

# 19. Frontend Information Architecture

## 19.1 School Portal pages

- Login
- Command Center
- Calendar
- Students & Attendance
- Meal History
- Surplus Radar
- Daily Forecast
- Preparation Planner
- Recovery Partners
- Communication
- Confirm Surplus
- Pickups
- Impact Analytics
- Audit History
- Settings
- AI Copilot drawer

## 19.2 Recovery Partner pages

- Partner Dashboard
- Capacity Calendar
- Potential Alerts
- Confirmed Requests
- Map
- Messages
- Pickup Management
- Distribution Reports
- Profile
- Food Rules
- Audit History
- AI Copilot drawer

## 19.3 Admin pages

- Network Overview
- School Verification
- Partner Verification
- Data Quality
- Model Monitoring
- Safety Incidents
- Audit Logs
- Impact Validation
- Model Versions
- System Settings

---

# 20. Visual and UX Specification

## 20.1 Design goals

The frontend should look like a real operations intelligence platform.

It should feel:

- modern;
- trustworthy;
- clear;
- high-impact;
- data-rich without being cluttered;
- visually memorable.

## 20.2 Key visual moments

- animated surplus-risk map;
- calendar risk overlay;
- prediction interval graph;
- current plan versus AI plan;
- partner match cards;
- pickup timeline;
- AI transparency panel;
- audit timeline;
- prevented versus recovered impact counters.

## 20.3 Accessibility

- labels in addition to color;
- readable contrast;
- keyboard navigation where feasible;
- clear focus states;
- plain-language explanations;
- responsive design.

## 20.4 Required states

Every major component must support:

- loading;
- empty;
- success;
- warning;
- error;
- insufficient data;
- manual mode;
- AI unavailable.

---

# 21. Security, Privacy, and Access Control

## 21.1 Data minimization

Use aggregated attendance rather than student names.

Do not collect:

- medical details;
- personal student profiles;
- unnecessary household information;
- sensitive identity data.

## 21.2 Role-based access

Every endpoint and action must check authorization.

## 21.3 Security requirements

- hashed passwords or managed authentication;
- secure sessions;
- server-side validation;
- audit logs;
- input sanitization;
- rate limiting where feasible;
- protected admin routes;
- no secrets in client code;
- environment variables;
- restricted file types.

## 21.4 Privacy explanation

The demo should state:

> SurplusSync Plus forecasts using aggregated operational data and does not need individual student identities.

---

# 22. Food Safety and Operational Responsibility

## 22.1 AI limitation

The AI cannot decide that food is legally safe.

## 22.2 Human checklist

A qualified person must confirm:

- food is untouched;
- packaging is acceptable;
- time is recorded;
- holding conditions are known;
- allergens are listed;
- partner accepts the category;
- pickup deadline is valid.

## 22.3 Uncertain cases

If required information is missing:

- mark as unresolved;
- do not auto-match;
- escalate for human review.

## 22.4 Alert wording

Before confirmation:

> Potential surplus forecast — not a confirmed donation.

After confirmation:

> Human-confirmed potentially recoverable surplus — partner review required.

---

# 23. Responsible AI Risks and Mitigations

## 23.1 Underproduction

**Risk:** Students may not receive meals.

**Mitigation:**

- shortage penalty;
- safety floor;
- interval-based buffer;
- human approval;
- manual override;
- alert when confidence is low.

## 23.2 Overconfidence

**Risk:** Users treat model output as fact.

**Mitigation:**

- intervals;
- uncertainty language;
- known limitations;
- calibration;
- no guaranteed language.

## 23.3 Data inequality

**Risk:** Schools with poor records receive worse predictions.

**Mitigation:**

- data-quality score;
- cold-start model;
- low-confidence warning;
- manual mode;
- administrator support.

## 23.4 Historical bias

**Risk:** Past attendance patterns may reflect exclusion.

**Mitigation:**

- aggregated inputs;
- fairness review;
- avoid interpreting absence as lack of need;
- protect service floor;
- allow local context overrides.

## 23.5 Partner ranking bias

**Risk:** Large partners dominate.

**Mitigation:**

- compatibility and capacity constraints;
- transparency;
- human selection;
- rotation or fairness option;
- reliability based on documented outcomes.

## 23.6 False donation expectations

**Risk:** Partner prepares for food that never appears.

**Mitigation:**

- forecast labels;
- quantity range;
- tentative reservation;
- same-day confirmation;
- cancellation workflow.

## 23.7 Copilot misuse

**Risk:** Natural-language command changes data incorrectly.

**Mitigation:**

- permissions;
- action preview;
- explicit approval;
- audit logs;
- undo;
- human-only actions.

---

# 24. Analytics and Impact

## 24.1 School metrics

- forecast accuracy;
- preparation accuracy;
- overproduction;
- underproduction;
- meal availability;
- prevented surplus;
- recoverable surplus;
- nonrecoverable waste;
- cost savings;
- override frequency.

## 24.2 Partner metrics

- alerts received;
- reservations;
- confirmed pickups;
- pickup success;
- quantity collected;
- response time;
- decline reasons;
- distribution outcome.

## 24.3 System metrics

- total schools;
- total partners;
- active forecasts;
- false alerts;
- calibration;
- low-data schools;
- incidents;
- partner coverage gaps.

## 24.4 Impact integrity

Never count the same meal as:

- prevented and recovered;
- recovered and discarded;
- forecast and confirmed.

Every impact number must have a clear source.

---

# 25. Demo Scenario

## 25.1 Demo school

Use one realistic U.S. public school or district scenario.

Example:

- 820 registered students;
- 760 meal-eligible;
- exam day;
- Grade 10 field trip;
- early dismissal;
- weather disruption;
- five menu components;
- three nearby recovery partners.

## 25.2 Demo sequence

1. Open School Command Center.
2. Show upcoming calendar events.
3. Surplus Radar flags Thursday.
4. Open the AI transparency panel.
5. Show expected attendance and interval.
6. Show menu-level demand.
7. Compare normal plan, rule baseline, ML baseline, and SurplusSync Plus.
8. Ask Copilot why the day is risky.
9. Ask Copilot to simulate attendance of 540.
10. Ask Copilot to update expected attendance.
11. Review action preview.
12. Approve update.
13. Forecast recalculates.
14. Copilot drafts potential alerts.
15. Human approves sending.
16. Partner tentatively reserves capacity.
17. School approves final preparation plan.
18. Same-day actual surplus is entered.
19. Human completes recovery checklist.
20. AI ranks partners.
21. Manager overrides the top match due to vehicle unavailability.
22. Second partner accepts.
23. Map displays pickup.
24. Pickup is completed.
25. Impact dashboard shows:
   - prevented surplus;
   - recovered surplus;
   - nonrecoverable waste;
   - students served;
   - model accuracy;
   - audit history.

---

# 26. Testing Plan

## 26.1 Unit tests

- feature engineering;
- forecast calculation;
- optimizer constraints;
- permission checks;
- impact accounting;
- partner compatibility;
- audit logging.

## 26.2 Integration tests

- calendar update → forecast rerun;
- attendance correction → recommendation update;
- alert → partner reservation;
- confirmed surplus → partner matching;
- Copilot proposal → approval → execution;
- override → audit log.

## 26.3 End-to-end tests

- complete school workflow;
- complete partner workflow;
- manual mode;
- AI unavailable;
- low-data warning;
- unsafe or incomplete surplus record;
- failed pickup;
- cancellation.

## 26.4 ML tests

- no time leakage;
- reproducible split;
- baseline comparison;
- interval coverage;
- out-of-distribution warning;
- robustness to missing fields;
- calibration.

## 26.5 UX tests

- dashboard understood in five seconds;
- judge can identify:
  - risk;
  - recommendation;
  - uncertainty;
  - human decision;
  - partner status.

---

# 27. Build Phases

## Phase 0 — Freeze Scope

- [ ] Approve this specification.
- [ ] Confirm team roles.
- [ ] Confirm technology stack.
- [ ] Confirm demo geography.
- [ ] Select demo school/district.
- [ ] Define non-goals.

## Phase 1 — Repository and Architecture

- [ ] Create repository.
- [ ] Add README.
- [ ] Add issue tracker.
- [ ] Add branch strategy.
- [ ] Add environment templates.
- [ ] Add database schema.
- [ ] Add third-party notices.
- [ ] Add data dictionary.

## Phase 2 — Data

- [ ] Gather U.S. public school data.
- [ ] Gather calendar.
- [ ] Gather weather.
- [ ] Gather partner locations.
- [ ] Define synthetic generation method.
- [ ] Generate meal history.
- [ ] Generate attendance history.
- [ ] Create held-out test set.
- [ ] Label provenance.

## Phase 3 — ML Baselines

- [ ] Recent average.
- [ ] Same weekday.
- [ ] Rule-based calendar model.
- [ ] Standard tabular model.
- [ ] Evaluation notebook.
- [ ] Baseline comparison chart.

## Phase 4 — SurplusSync Plus Model

- [ ] Attendance model.
- [ ] Menu-level demand model.
- [ ] Prediction intervals.
- [ ] Calibration.
- [ ] Optimizer.
- [ ] Risk classifier.
- [ ] Similar-day retrieval.
- [ ] Explanation layer.
- [ ] Model API.

## Phase 5 — Backend

- [ ] Authentication.
- [ ] Roles and permissions.
- [ ] School endpoints.
- [ ] Calendar endpoints.
- [ ] Attendance endpoints.
- [ ] Meal endpoints.
- [ ] Forecast endpoints.
- [ ] Partner endpoints.
- [ ] Messaging.
- [ ] Pickup.
- [ ] Audit logs.
- [ ] Copilot action proposals.

## Phase 6 — Frontend

- [ ] School dashboard.
- [ ] Calendar.
- [ ] Attendance.
- [ ] Meal history.
- [ ] Surplus Radar.
- [ ] Daily forecast.
- [ ] Partner portal.
- [ ] Map.
- [ ] Communication.
- [ ] Pickup tracking.
- [ ] Admin portal.
- [ ] Transparency panel.
- [ ] Override flow.
- [ ] Copilot.

## Phase 7 — Integration

- [ ] Connect frontend to backend.
- [ ] Connect backend to model API.
- [ ] Connect corrections to reruns.
- [ ] Connect alerts to partner portal.
- [ ] Connect map to matches.
- [ ] Connect Copilot to action system.
- [ ] Connect audit history.

## Phase 8 — Validation

- [ ] Run held-out evaluation.
- [ ] Compare baselines.
- [ ] Validate impact accounting.
- [ ] Test human controls.
- [ ] Test manual mode.
- [ ] Test low-confidence scenarios.
- [ ] Document limitations.

## Phase 9 — Presentation

- [ ] Final UI polish.
- [ ] Demo data reset.
- [ ] Demo script.
- [ ] Architecture diagram.
- [ ] Model comparison visuals.
- [ ] Responsible AI slide.
- [ ] 3–5 minute video.
- [ ] Devpost text.
- [ ] Tool disclosure.
- [ ] Data disclosure.
- [ ] Qualifier code.
- [ ] Final submission check.

---

# 28. Team Workstreams

## Workstream A — Product and Research

- official requirements;
- problem evidence;
- data sources;
- partner research;
- food-safety limitations;
- product specification;
- Devpost writing.

## Workstream B — Data and ML

- data pipeline;
- synthetic generation;
- baselines;
- forecasting;
- calibration;
- optimization;
- evaluation;
- explainability.

## Workstream C — Backend

- database;
- APIs;
- permissions;
- workflows;
- messaging;
- audit logs;
- Copilot actions;
- model integration.

## Workstream D — Frontend and Experience

- design system;
- dashboards;
- map;
- portals;
- communication;
- Copilot interface;
- animations;
- responsive design.

## Workstream E — Pitch and Quality

- testing;
- demo scenario;
- video;
- visuals;
- architecture;
- responsible AI;
- final checklist.

---

# 29. Definition of Done

## 29.1 Product

- [ ] School can manage calendar, attendance, and meal history.
- [ ] School can edit incorrect values with audit history.
- [ ] Model predicts attendance and menu-level demand.
- [ ] Forecast shows intervals and risk.
- [ ] Model is compared against simple baselines.
- [ ] Manager can approve, modify, reject, or override.
- [ ] Surplus Radar displays future risk.
- [ ] Recovery partners maintain capacity and rules.
- [ ] Potential alerts are provisional.
- [ ] Confirmed surplus requires human checklist.
- [ ] AI ranks partners.
- [ ] Human selects final partner.
- [ ] Messaging works.
- [ ] Map shows entities and route.
- [ ] Pickup status works.
- [ ] Copilot explains and proposes actions.
- [ ] Consequential Copilot actions require approval.
- [ ] Manual mode exists.
- [ ] Audit history is visible.
- [ ] Impact is separated correctly.

## 29.2 AI

- [ ] No time leakage.
- [ ] Baselines implemented.
- [ ] Held-out test results reported.
- [ ] Uncertainty evaluated.
- [ ] Confidence is not decorative.
- [ ] Model limitations disclosed.
- [ ] Synthetic data labeled.
- [ ] Explanations available.
- [ ] Human override is functional.
- [ ] Safety floor is enforced.

## 29.3 Competition

- [ ] Problem is explained through a concrete user.
- [ ] Why AI is necessary is demonstrated.
- [ ] Architecture is understandable.
- [ ] Impact is measurable.
- [ ] Human in the loop is visible in the demo.
- [ ] Responsible AI risk is specific.
- [ ] Demo link works.
- [ ] Video is 3–5 minutes.
- [ ] All tools are disclosed.
- [ ] All data sources are disclosed.
- [ ] Qualifier code is entered exactly.
- [ ] Final submission is completed before deadline.

---

# 30. Risks and Countermeasures

| Risk | Countermeasure |
|---|---|
| AI appears unnecessary | Baseline comparison and menu-level event interaction |
| Synthetic data appears manipulated | Transparent generation, noise, held-out test set |
| Under-ordering harms students | Safety floor, shortage penalty, human approval |
| Food safety claims are unsafe | Human-only recovery confirmation |
| Redistribution conflicts with prevention | Separate preventable and unavoidable surplus |
| Too many features | Protect primary demo workflow |
| Frontend overshadows ML | Show real evaluation and transparency |
| ML overshadows usability | Clear action-oriented UI |
| Partner data is unavailable | Use public partner locations and synthetic capacity labels |
| Copilot feels like a chatbot wrapper | Structured actions, permissions, previews, audit logs |
| Judge asks what is original | Emphasize operational layer, uncertainty, optimization, and recovery coordination |
| Map is only visual decoration | Use it for matching, capacity, and pickup workflow |
| Confidence scores are fake | Use evaluated prediction intervals and calibration |
| Manual corrections corrupt data | Audit logs, provenance, reviewed retraining |

---

# 31. Open Questions

Resolve these before final integration:

- [ ] Which U.S. school or district will be used?
- [ ] Which public data sources are available?
- [ ] Which partner organizations will appear in the demo?
- [ ] Which framework will be used?
- [ ] Which mapping provider will be used?
- [ ] Which model will be the primary model?
- [ ] What service-level target will be used?
- [ ] What exact food categories will be predicted?
- [ ] How will synthetic data assumptions be validated?
- [ ] What actions can the Copilot execute?
- [ ] Which actions remain human-only?
- [ ] Which screens are essential for the video?
- [ ] What is the final product tagline?

---

# 32. Final Pitch Positioning

## Recommended opening

> A cafeteria manager does not need another report showing yesterday’s waste. She needs to know, before tomorrow’s food is prepared, how many students are likely to eat—and what to do if the forecast is uncertain.

## Recommended core line

> SurplusSync Plus predicts school meal demand, protects students from shortages, and connects unavoidable safe surplus with verified recovery partners before it becomes waste.

## Recommended closing

> We are not measuring food after it reaches the bin. We are helping schools prevent the waste, protect every student meal, and recover what could not be prevented.

---

# 33. Immediate Next Actions

Complete these first:

1. Freeze the technology stack.
2. Select the U.S. demo school or district.
3. Create the repository and issue board.
4. Implement the database schema.
5. Create the data dictionary.
6. Collect public calendar, enrollment, weather, and partner-location data.
7. Generate realistic synthetic attendance and meal history.
8. Implement the recent-average and calendar-rule baselines.
9. Build the first attendance and demand model.
10. Build a minimal School Command Center that displays one real forecast.
11. Add prediction interval and “Why this prediction?”
12. Add one human override flow.
13. Add three recovery partners with capacity.
14. Build the first potential-surplus alert.
15. Demonstrate the complete school → forecast → approval → partner sequence before polishing the rest.

---

**End of specification**
