# Roadmap — AI Recruiter Agent Swarm

> **Hackathon Timeline:** 3 June 2026 -> 2 July 2026 (Submission)
> **Grand Finale:** 22 July 2026

---

## Progress Snapshot

```
Phase 0: [####################] 100%  — Ideation & Problem Validation
Phase 1: [####################] 100%  — Architecture Design
Phase 2: [####################] 100%  — Pitch Deck & Visuals
Phase 3: [....................]   0%  — Documentation & Submission
```

---

## Phase 0: Ideation & Problem Validation

**Goal:** Validate the problem, define scope, research competition
**Duration:** 2 days
**Deadline:** 17 June 2026
**Status:** In Progress

### Tasks

- [x] Identify the core problem (traditional ATS misses good candidates)
- [x] Define the multi-agent swarm concept
- [ ] Research existing solutions (ATS platforms, AI recruiting tools)
- [ ] Identify gaps in current market offerings
- [x] Decide positioning for India Runs judging criteria
- [ ] Define success metrics for the solution

### Deliverables

- [ ] Competitive analysis table (5+ competitors)
- [ ] Problem validation brief
- [ ] Target user persona(s)

### Notes

- Major ATS players: Greenhouse, Lever, Workday, SmartRecruiters
- AI recruiting tools: Ideal, HireVue, Pymetrics, Eightfold
- Key gap: None use multi-agent swarms with voice screening in regional languages

---

## Phase 1: Architecture Design

**Goal:** Design complete system architecture with agent specifications
**Duration:** 5 days
**Deadline:** 22 June 2026
**Status:** Completed

### Tasks

- [x] Design Orchestrator Agent logic (task routing, state machine, escalation)
- [x] Design Sourcer Agent (multi-source crawling, de-duplication, confidence ranking)
- [x] Design Matcher Agent (5-dimension scoring, transferable skill detection, explainable AI)
- [x] Design Screener Agent (voice pipeline, Hinglish/regional support, dynamic questioning)
- [x] Design Scheduler Agent (calendar integration, negotiation, reminders)
- [x] Define agent-to-agent communication protocol (async message broker, standard envelope)
- [x] Design Memory & Context Layer (Vector DB schema, Redis cache, PostgreSQL schema)
- [x] Define escalation rules (12 scenarios, severity matrix, auto-resolution flows)
- [x] Plan API contracts between agents (full request/response specs for all interactions)
- [x] Map data flow end-to-end (JD input -> final shortlist)

### Deliverables

- [x] System architecture diagram (Mermaid — in docs/diagrams.md)
- [x] Agent specification documents (docs/agent-specs.md + agent stubs in src/)
- [x] Data flow diagram (Mermaid — in docs/diagrams.md)
- [x] API contract definitions (docs/agent-communication.md)
- [x] Tech stack decision record (docs/tech-stack.md)

### Key Decisions to Make

- Orchestration framework: LangChain vs CrewAI vs AutoGen vs custom
- Voice model: Sarvam AI vs Bhashini vs Whisper fine-tune
- Embedding model: BGE-M3 vs multilingual E5 vs fine-tuned IndicBERT
- Vector DB: Qdrant vs ChromaDB vs Weaviate vs Pinecone
- LLM for agents: Gemini 1.5 Pro vs GPT-4o vs open-source fine-tuned

---

## Phase 2: Pitch Deck & Visuals

**Goal:** Create compelling pitch deck, user journey, and visual assets
**Duration:** 5 days
**Deadline:** 27 June 2026
**Status:** Completed

### Tasks

- [x] Structure pitch deck (problem -> solution -> architecture -> impact)
- [x] Create slide-by-slide content with India-specific narrative
- [x] Design system architecture diagram (Mermaid + HTML deck)
- [x] Design agent interaction flow diagram (Mermaid sequence diagrams)
- [x] Create user journey map (persona-based Priya walkthrough)
- [x] Design mockups/wireframes (4 screens: dashboard, shortlist, scoring, assessment)
- [x] Write compelling problem narrative (India-specific context)
- [x] Quantify impact (10 min vs 5 days, 70% cost reduction, 34% accuracy gain)
- [x] Define future roadmap (Q3 2026 through Q2 2027)
- [x] Record demo video script (3:45 script with timestamps)

### Deliverables

- [x] Pitch Deck (HTML) — 12 slides, printable to PDF (assets/pitch-deck.html)
- [x] System architecture diagram (docs/diagrams.md + architecture.md)
- [x] User journey map (docs/user-journey.md)
- [x] Mockups/wireframes — 4 screens (assets/dashboard-mockup.html)
- [x] Demo video script (docs/demo-video-script.md)

### Pitch Deck Structure (Proposed)

| Slide | Content |
|-------|---------|
| 1 | Title slide - "AI Recruiter Agent Swarm" |
| 2 | The Problem - "India's hiring is broken" |
| 3 | Why Now - AI maturity + India's talent boom |
| 4 | Our Solution - Multi-agent swarm overview |
| 5 | How It Works - Agent interactions |
| 6 | Architecture - System design |
| 7 | Key Differentiator - Voice screening in Hinglish |
| 8 | Impact Metrics - Speed, quality, cost savings |
| 9 | Market Opportunity - India's recruitment market |
| 10 | Roadmap - Beyond the hackathon |
| 11 | About Me - Builder, not just a presenter |

---

## Phase 3: Documentation & Submission

**Goal:** Polish all deliverables, prepare submission, submit
**Duration:** 3 days
**Deadline:** 1 July 2026
**Status:** Not Started

### Tasks

- [ ] Final review of all documents
- [ ] Proofread pitch deck
- [ ] Create submission video (if required)
- [ ] Prepare GitHub repository - clean, well-documented
- [ ] Write submission description
- [ ] Double-check submission checklist against requirements
- [ ] Submit before deadline

### Deliverables

- [x] GitHub repository with README, ROADMAP, PROGRESS
- [ ] Final pitch deck PDF
- [ ] Architecture diagram(s)
- [ ] Submission form filled

### Submission Checklist (from challenge page)

- [ ] The Pitch Deck - organized story as PDF
- [ ] Your Target - clearly state which problem statement
- [ ] The Core Solution - detailed breakdown of AI-native idea
- [ ] The User Journey - step-by-step interaction map
- [ ] Visuals - optional mockups, wireframes

---

## Post-Submission: Preparation for Grand Finale

**Goal:** Prepare for live presentation on 22 July 2026
**Duration:** 20 days (buffer)
**Deadline:** 22 July 2026
**Status:** Not Started

### Tasks

- [ ] Prepare 5-minute pitch presentation
- [ ] Prepare Q&A document (anticipated questions)
- [ ] Practice presentation delivery
- [ ] Prepare live demo if applicable
- [ ] Prepare technical deep-dive (if judges ask)
- [ ] Plan answers about feasibility, scalability, impact

---

## Key Milestones Summary

| Milestone | Date | Phase |
|-----------|------|-------|
| Project start | 16 June 2026 | Phase 0 |
| Problem validation complete | 17 June 2026 | Phase 0 |
| Architecture design complete | 22 June 2026 | Phase 1 |
| Pitch deck & visuals ready | 27 June 2026 | Phase 2 |
| All docs finalized | 1 July 2026 | Phase 3 |
| **Submission deadline** | **2 July 2026** | Phase 3 |
| Evaluation phase | 3-16 July 2026 | - |
| **Grand Finale** | **22 July 2026** | - |

---

## Success Criteria

1. A clear, compelling problem statement rooted in India's hiring reality
2. A well-architected multi-agent system with defined agent roles
3. A professional pitch deck that tells a story
4. Clear differentiation from existing solutions
5. India-specific innovation (vernacular voice screening)
