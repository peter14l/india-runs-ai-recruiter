# Submission Description — AI Recruiter Agent Swarm

## Track: Track 2 — The Ideathon

## Problem Statement: Challenge 1 — The AI Systems Architect: Reimagining Work

### Elevator Pitch (max 200 words)

Traditional recruitment is broken. Keyword filters miss 70% of qualified candidates. Screening is slow, biased, and scales poorly. In India, where talent spans 22+ languages and Tier 2/3 cities hold untapped potential, the problem is amplified.

The AI Recruiter Agent Swarm replaces linear ATS filtering with an autonomous multi-agent system. Five specialized AI agents — Orchestrator, Sourcer, Matcher, Screener, and Scheduler — collaborate to source candidates from multiple platforms (LinkedIn, GitHub, Naukri), semantically match them to job descriptions (beyond keywords), conduct voice-based pre-screenings in Hinglish and regional languages, and autonomously schedule interviews.

Key differentiators: (1) multi-agent coordination with state management and human escalation, (2) voice screening in Indian languages via Sarvam AI/Bhashini, (3) semantic matching that detects transferable skills, and (4) continuous learning from recruiter feedback.

This system is built for India-first hiring — bringing quality talent discovery to Tier 2/3 cities by removing language barriers and keyword gatekeeping.

### Core Solution

The system uses a hierarchical swarm architecture:

- **Orchestrator Agent** (brain): routes tasks, maintains conversation state, decides escalation
- **Sourcer Agent**: crawls LinkedIn, GitHub, Naukri, and internal DBs autonomously
- **Matcher Agent**: embeds JDs + profiles using BGE-M3, computes 5-dimension relevance scores
- **Screener Agent**: conducts AI voice interviews in Hinglish using Sarvam AI STT/TTS + Whisper
- **Scheduler Agent**: syncs calendars, negotiates slots, sends reminders via email/WhatsApp

All agents communicate via an async message broker with a standard envelope format. The system stores candidate embeddings in Qdrant vector DB, maintains session state in Redis, and persists data in PostgreSQL.

### Target Users

- Recruiters at Indian companies (startups to enterprises)
- HR teams looking to scale hiring without scaling headcount
- Candidates from Tier 2/3 cities who speak English + regional languages

### Submission Assets

- **PDF Pitch Deck**: `assets/pitch-deck.pdf`
- **Visuals (HTML Dashboard Mockup)**: `assets/dashboard-mockup.html`
- **System Architecture**: `docs/architecture.md`
- **Agent Specifications**: `docs/agent-specs.md`
- **User Journey**: `docs/user-journey.md`
- **Demo Video Script**: `docs/demo-video-script.md`
- **All Documents**: See GitHub repo docs/ folder
