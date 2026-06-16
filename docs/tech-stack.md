# Tech Stack Decision Record

> Documenting key technology choices and their rationale.

---

## 1. Agent Orchestration Framework

**Decision:** CrewAI

**Alternatives considered:**
- AutoGen (Microsoft) - More complex, better for agent-to-agent debate scenarios
- LangGraph - Lower level, more flexible but more boilerplate
- Custom implementation - Full control but too time-consuming

**Rationale:** CrewAI provides the best balance of hierarchical agent management, tool use, and simplicity. Its "crew" concept maps directly to our swarm architecture. AutoGen would be overkill since our agents don't need to negotiate/debate — they follow a clear pipeline.

**Status:** DECIDED

---

## 2. Voice Model

**Decision:** Sarvam AI

**Alternatives considered:**
- Bhashini - Government DPI, free, but higher latency
- Azure Speech - Good quality, better for English, weaker for Indic languages
- Whisper fine-tune - Most control, but requires GPU infrastructure

**Rationale:** Sarvam has the best Indic language support (including Hinglish, which is the primary use case). Their voice models are specifically trained on Indian accents and code-mixed speech. Bhashini is a backup option for zero-cost scenarios.

**Status:** PENDING (need to test both Sarvam and Bhashini APIs)

---

## 3. Embedding Model

**Decision:** BGE-M3

**Alternatives considered:**
- multilingual-E5-large - Good but larger, slower
- fine-tuned IndicBERT - Better for pure Indic languages, weaker for English
- OpenAI text-embedding-3 - Excellent quality but API cost and data privacy concerns

**Rationale:** BGE-M3 offers the best balance of multilingual support (crucial for Indian names, Hinglish JDs, mixed-language resumes), embedding quality, and inference speed. It supports 100+ languages and handles code-switching well.

**Status:** DECIDED

---

## 4. Vector Database

**Decision:** Qdrant

**Alternatives considered:**
- ChromaDB - Simpler for prototyping, but limited production features
- Pinecone - Managed, expensive for prototyping
- Weaviate - Good but heavier infrastructure

**Rationale:** Qdrant offers the best balance of performance, filtering support (needed for skill/location/experience filters), and self-hosting capability. Binary quantization support reduces memory usage by 30-50%.

**Status:** DECIDED

---

## 5. LLM for Agents

**Decision:** Gemini 1.5 Pro

**Alternatives considered:**
- GPT-4o - Excellent but expensive, weaker multilingual support
- Claude 3.5 Sonnet - Great reasoning but no Indic language optimization
- Open-source fine-tuned (Llama 3, Mistral) - More control but needs infrastructure

**Rationale:** Gemini 1.5 Pro has the best multilingual performance, especially for Indian languages. Its 1M token context window is useful for processing large JDs and multiple candidate profiles. Lower cost than GPT-4o for equivalent quality.

**Status:** DECIDED (with GPT-4o as fallback)

---

## 6. Backend Framework

**Decision:** FastAPI

**Alternatives considered:**
- Django - Heavy for this purpose
- Flask - Too minimal, missing async support
- Node.js/Express - Not aligned with Python ML ecosystem

**Rationale:** FastAPI is Python-native (integrates seamlessly with ML libraries), async-first (important for concurrent agent operations), auto-generates OpenAPI docs, and has excellent performance.

**Status:** DECIDED

---

## 7. Frontend (Demo Dashboard)

**Decision:** Streamlit

**Alternatives considered:**
- React - Overkill for a demo/prototype
- Gradio - Good for ML demos but less customizable

**Rationale:** Streamlit allows rapid prototyping of the recruiter dashboard with minimal code. Since the primary deliverable is a pitch deck (not a working product), Streamlit is sufficient for the demo.

**Status:** PROVISIONAL (could switch to React if time permits)

---

## 8. Telephony for Voice Calls

**Decision:** Twilio

**Alternatives considered:**
- Vonage - Similar features, smaller market share
- Plivo - Cheaper but fewer features

**Rationale:** Twilio has the best documentation, SDK support, and reliability for programmatic voice calls. Pay-as-you-go pricing works for the prototype phase.

**Status:** PROVISIONAL

---

## Summary Table

| Component | Decision | Status |
|-----------|----------|--------|
| Agent Framework | CrewAI | DECIDED |
| Voice Model | Sarvam AI | PENDING |
| Embedding Model | BGE-M3 | DECIDED |
| Vector DB | Qdrant | DECIDED |
| LLM | Gemini 1.5 Pro | DECIDED |
| Backend | FastAPI | DECIDED |
| Frontend (demo) | Streamlit | PROVISIONAL |
| Telephony | Twilio | PROVISIONAL |
| Containerization | Docker | DECIDED |
