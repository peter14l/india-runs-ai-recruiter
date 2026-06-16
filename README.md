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
├── docs/
│   ├── architecture.md
│   ├── agent-specs.md
│   ├── data-flow.md
│   ├── tech-stack.md
│   ├── user-journey.md
│   └── pitch-deck.md
├── src/
│   └── (in future phases)
└── assets/
    └── (diagrams, wireframes, etc.)
```

---

## 🛤️ Current Status

See [ROADMAP.md](./ROADMAP.md) for the full phased plan and [PROGRESS.md](./PROGRESS.md) for real-time progress tracking.

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

## 🛠️ Built With (Planned Stack)

- **Orchestration:** LangChain / CrewAI / AutoGen
- **Voice:** Sarvam AI / Bhashini for Hinglish + regional languages
- **Embeddings:** BGE-M3 / multilingual sentence transformers
- **Vector DB:** Qdrant / ChromaDB
- **LLM:** Gemini / GPT-4 / open-source fine-tuned model
- **Backend:** FastAPI + Python
- **Frontend:** Streamlit / React (for demo dashboard)

---

## 👤 About Me

A Class 12 graduate proficient in building with AI tools. Participating in **India Runs** by Redrob AI to build what next India runs on.

---

> **India Runs** — India's most open hackathon by Redrob AI. ₹50 Lakh+ prize pool. Open to all.
