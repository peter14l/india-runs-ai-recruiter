# AI Recruiter Agent Swarm

> **India Runs Hackathon — Track 2, Challenge 1: AI Systems Architect**
> Building what next India runs on.

An autonomous multi-agent AI system that revolutionizes talent acquisition. Instead of traditional keyword-based filtering, this system uses a coordinated **swarm of specialized AI agents** that deeply understand job descriptions, semantically rank candidates, conduct voice-based screenings, and autonomously manage the entire hiring pipeline — from sourcing to shortlisting.

---

## 🧠 The Big Idea

Recruiters drown in profiles. Keyword filters miss hidden gems. Good candidates fall through the cracks.

The **AI Recruiter Agent Swarm** replaces linear, keyword-based filtering with an intelligent, autonomous system of coordinated AI agents — each specialized in one phase of recruitment — working together to find the perfect candidate for every role.

---

## 🏗️ System Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Orchestrator Agent                    │
│    (Coordinates all agents, maintains state, routes)     │
└────┬─────────┬─────────┬──────────┬──────────────────────┘
     │         │         │          │
     ▼         ▼         ▼          ▼
┌────────┐┌────────┐┌────────┐ ┌──────────┐
│ Sourcer ││Matcher ││Screener│ │ Scheduler│
│ Agent   ││Agent   ││Agent   │ │ Agent    │
└────────┘└────────┘└────────┘ └──────────┘
     │         │         │          │
     ▼         ▼         ▼          ▼
┌──────────────────────────────────────────┐
│            Memory & Context Layer         │
│   (Vector DB + Knowledge Graph + Cache)   │
└──────────────────────────────────────────┘
```

---

## 🤖 Agents Defined

| Agent | Role | Capabilities |
|-------|------|-------------|
| **Orchestrator** | Brain of the system | Routes tasks, maintains conversation state, decides when to escalate to humans |
| **Sourcer Agent** | Profile discovery | Crawls job portals, GitHub, LinkedIn, internal DBs. Learns new sources over time |
| **Matcher Agent** | Semantic ranking | Embeds JDs + profiles, computes relevance scores beyond keyword match. Detects transferable skills |
| **Screener Agent** | Voice-based pre-interview | Conducts natural voice interviews in Hinglish/regional languages. Assesses communication, cultural fit, and technical basics |
| **Scheduler Agent** | Logistics coordinator | Syncs calendars, sends reminders, handles rescheduling. Negotiates time slots autonomously |

---

## 🎯 Key Differentiators

| Feature | Traditional ATS | This System |
|---------|----------------|-------------|
| Matching | Keyword-based | Semantic + behavioral signal analysis |
| Screening | Manual phone screen | AI-driven voice conversation in Hinglish/regional languages |
| Sourcing | One database | Autonomous multi-source crawling |
| Coordination | Manual handoffs | Agent-to-agent orchestration |
| Language | English only | English + Hinglish + regional languages |
| Learning | Static rules | Continuous improvement from feedback |

---

## 📁 Project Structure

```
ai-recruiter-swarm/
├── README.md
├── ROADMAP.md
├── PROGRESS.md
├── demo.py                          # Working CLI demo — run `python demo.py`
├── docs/
│   ├── architecture.md              # Multi-agent system architecture
│   ├── agent-specs.md               # Detailed agent specifications
│   ├── data-flow.md                 # Data pipelines & message bus design
│   ├── tech-stack.md                # Technology choices & rationale
│   ├── user-journey.md              # End-to-end user journey
│   ├── demo-video-script.md         # Script for demo video
│   ├── escalation-rules.md          # 12 human escalation rules
│   └── submission-description.md    # Ready-to-copy text for hack2skill portal
├── assets/
│   ├── pitch-deck.html              # HTML source for 12-slide pitch deck
│   ├── pitch-deck.pdf               # PDF pitch deck (submission asset)
│   ├── pitch-deck.pptx              # PPTX pitch deck (secondary)
│   ├── dashboard-mockup.html        # 4-screen recruiter dashboard mockup
│   ├── generate_pdf.py              # PDF generation script
│   └── submission.pptx              # Filled mandatory template (open in PPT to export PDF)
└── (IDEATHON) Track 1 Submission Template.pptx   # Original template from hack2skill
```

---

## 🏁 Submission Status

**Track 2 — Challenge 1: The AI Systems Architect**

- [x] Ideation & Problem Definition
- [x] Architecture Design (5-agent swarm + orchestrator)
- [x] Pitch Deck (12-slide PDF + PPTX)
- [x] Documentation (architecture, specs, data flow, tech stack, user journey)
- [x] Working CLI Demo (`python demo.py` — full pipeline simulation)
- [x] Submission Template Filled (`assets/submission.pptx`)
- [x] Dashboard Mockup (`assets/dashboard-mockup.html`)
- [x] **Export `submission.pptx` → PDF (`assets/submission.pdf`)**
- [x] **Submitted on hack2skill (Attempt 1)**
- [ ] **Grand Finale: 22 July 2026**

> See [ROADMAP.md](./ROADMAP.md) for the full phased plan and [PROGRESS.md](./PROGRESS.md) for detailed progress.

---

## 📅 Hackathon Timeline

| Milestone | Date |
|-----------|------|
| Registrations Open | 19 May 2026 |
| Ideathon Submissions Begin | 3 June 2026 |
| Registrations Close | 28 June 2026 |
| Ideathon Submissions Close | 2 July 2026 |
| Evaluation Phase | 3–16 July 2026 |
| Grand Finale (Virtual) | 22 July 2026 |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Agent Framework | CrewAI / AutoGen |
| LLM | Gemini 1.5 Pro (primary), GPT-4o (fallback) |
| Voice | Sarvam AI (STT/TTS), fine-tuned Whisper |
| Embeddings | BGE-M3 multilingual |
| Vector DB | Qdrant |
| Backend | FastAPI + Python |
| Message Bus | Redis Pub/Sub |
| Cache | Redis |
| Storage | PostgreSQL |
| Communication | Async message bus (standard envelope format)

---

## 👤 About Me

A Class 12 graduate proficient in building with AI tools. Participating in **India Runs** by Redrob AI to build what next India runs on.

---

## 🎬 Try the Demo

```bash
python demo.py
```

Runs the full 5-agent pipeline simulation in ~8 seconds — shows agent communication logs, scored candidate tables, and final shortlist.

---

> **India Runs** — India's most open hackathon by Redrob AI. ₹50 Lakh+ prize pool. Open to all.
