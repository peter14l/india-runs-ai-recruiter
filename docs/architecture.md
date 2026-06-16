# System Architecture — AI Recruiter Agent Swarm

---

## High-Level Overview

The AI Recruiter Agent Swarm is a multi-agent system where specialized AI agents collaborate autonomously to handle the end-to-end recruitment pipeline. An Orchestrator Agent coordinates all agents, manages state, and decides when human intervention is needed.

---

## Architecture Diagram

`
                              USER INTERFACE
                              (Dashboard / API)
                                    |
                                    v
                        +-----------------------+
                        |   Orchestrator Agent  |
                        |  (Task Router +       |
                        |   State Manager +     |
                        |   Human Escalation)   |
                        +-----------+-----------+
                                    |
             +----------------------+----------------------+
             |          |          |          |            |
             v          v          v          v            |
     +-----------+ +-----------+ +-----------+ +--------+  |
     |  Sourcer  | |  Matcher  | | Screener | |Scheduler|  |
     |  Agent    | |  Agent    | | Agent    | | Agent   |  |
     +-----------+ +-----------+ +-----------+ +--------+  |
             |          |          |          |            |
             +----------+----------+----------+------------+
                                    |
                        +-----------------------+
                        |  Memory & Context     |
                        |  Layer                |
                        |  (Vector DB +         |
                        |   Knowledge Graph)    |
                        +-----------------------+
                                    |
                        +-----------------------+
                        |  External Integrations |
                        |  (LinkedIn, GitHub,    |
                        |   Email, Calendar,     |
                        |   ATS APIs)            |
                        +-----------------------+
`

---

## Agent Communication Flow

`
1. RECRUITER submits a Job Description via dashboard
       |
       v
2. ORCHESTRATOR parses the JD, extracts key requirements
       |
       +---> 3a. SOURCER Agent: Crawl job portals, GitHub, LinkedIn for matching profiles
       |          |
       |          +---> Returns candidate profiles with source URLs
       |
       +---> 3b. MATCHER Agent: Embed JD + candidate profiles, compute relevance scores
       |          |
       |          +---> Returns ranked shortlist with scores + reasoning
       |
       +---> 3c. SCREENER Agent: Conduct voice calls with top candidates
       |          |
       |          +---> Returns assessment report (communication, skills, cultural fit)
       |
       +---> 3d. SCHEDULER Agent: Coordinate interview slots with human recruiters
                  |
                  +---> Returns confirmed interview schedule
       |
       v
4. ORCHESTRATOR compiles final shortlist with all agent outputs
       |
       v
5. HUMAN RECRUITER reviews, provides feedback (which feeds back into learning loop)
`

---

## Technology Stack

### Layer 1: Orchestration & Agent Framework

| Component | Candidates | Rationale |
|-----------|------------|-----------|
| Agent Framework | CrewAI / AutoGen / LangGraph | CrewAI is simplest for hierarchical swarms; AutoGen better for complex agent negotiation |
| State Management | Redis + PostgreSQL | Redis for real-time state, PostgreSQL for persistent history |
| Message Queue | RabbitMQ / Redis PubSub | Async agent communication |

### Layer 2: AI & ML

| Component | Candidates | Rationale |
|-----------|------------|-----------|
| Embedding Model | BGE-M3 / multilingual-E5-large | Strong multilingual support (critical for Indian names, Hinglish JDs) |
| Vector Database | Qdrant / ChromaDB | Qdrant for production; ChromaDB for prototyping |
| LLM for Agents | Gemini 1.5 Pro / GPT-4o | Gemini has stronger multilingual + lower cost; GPT-4o for complex reasoning |
| Voice STT/TTS | Sarvam AI / Bhashini / Azure Speech | Sarvam has best Indic language support; Bhashini is government DPI |
| Voice Assessment | Fine-tuned Whisper + custom classifier | Detects fluency, confidence, communication patterns |

### Layer 3: Backend & Infrastructure

| Component | Choice | Rationale |
|-----------|--------|-----------|
| API Framework | FastAPI | Python-native, async, great DX |
| Task Queue | Celery + Redis | For long-running agent tasks |
| Containerization | Docker + Docker Compose | Reproducible development and deployment |
| Cloud (if deployed) | AWS / GCP / Azure | Any works; GCP has best Gemini integration |

---

## Data Flow

### Inbound Data
- Job Descriptions (text, PDF, URL)
- Candidate profiles (LinkedIn, GitHub, Naukri, internal DB)
- Recruiter feedback (ratings, comments, hiring decisions)

### Storage Schema
- **Vector Store:** Candidate embeddings, JD embeddings, skill embeddings
- **Relational DB:** Users (recruiters), Jobs, Candidates, Interviews, Feedback
- **Document Store:** Resumes (PDF), JD files, interview transcripts
- **Cache:** Recent searches, hot profiles, session state

### Outbound Data
- Ranked candidate shortlist
- Assessment reports
- Interview schedule
- Analytics dashboard
- API webhooks to existing ATS

---

## Security & Privacy Considerations

- All candidate data encrypted at rest and in transit
- PII handling: Masked in agent communications, only revealed to human recruiters at final stage
- Opt-in consent for voice screening (candidate agrees before call)
- GDPR/DPDP compliance for data storage and processing
- Audit trail for all agent decisions and human interventions

---

## Scalability Design

- **Horizontal scaling:** Each agent type can be deployed as independent microservices
- **Async processing:** Agents communicate via message queues, not synchronous calls
- **Caching:** Repeated JD-to-candidate matches are cached (same JD rarely seen twice, but similar patterns are)
- **Batch processing:** Sourcer Agent can batch-crawl during off-peak hours
- **Rate limiting:** External API calls (LinkedIn, GitHub) are rate-limited with retry logic
