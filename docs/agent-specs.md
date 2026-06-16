# Agent Specifications — AI Recruiter Agent Swarm

---

## 1. Orchestrator Agent

**Role:** The brain of the system. Coordinates all other agents, maintains conversation state, routes tasks, and decides when to escalate to humans.

### Personality & Tone
Professional, decisive, clear. Communicates status updates to the recruiter in natural language.

### Core Capabilities

| Capability | Description |
|------------|-------------|
| Task Routing | Parses incoming job descriptions and routes to appropriate agents in sequence |
| State Management | Maintains a global state of all ongoing recruitment pipelines |
| Progress Tracking | Reports real-time status to the recruiter dashboard |
| Human Escalation | Decides when a decision requires human judgment (e.g., tie-breaking between two equally matched candidates) |
| Feedback Integration | Incorporates recruiter feedback to adjust agent behavior |

### Input
- Job description (text, URL, or file)
- Recruiter commands and preferences
- Agent outputs

### Output
- Final ranked shortlist with supporting evidence
- Status updates
- Escalation requests

### Decision Logic (Pseudocode)

`
function processJob(jobDescription):
    state = createInitialState(jobDescription)
    
    candidates = SourcerAgent.search(jobDescription)
    state.addCandidates(candidates)
    
    rankedCandidates = MatcherAgent.rank(candidates, jobDescription)
    state.addRankings(rankedCandidates)
    
    topCandidates = rankedCandidates.top(threshold)
    for candidate in topCandidates:
        assessment = ScreenerAgent.assess(candidate, jobDescription)
        state.addAssessment(candidate, assessment)
    
    if recruiter.preferences.autoSchedule:
        schedule = SchedulerAgent.schedule(topCandidates)
        state.addSchedule(schedule)
    
    if state.requiresHumanReview():
        escalateToHuman(state.summary())
    else:
        return state.finalShortlist()
`

---

## 2. Sourcer Agent

**Role:** Prospector and scout. Discovers candidate profiles across multiple sources.

### Personality & Tone
Persistent, thorough, resourceful. Doesn't give up easily.

### Core Capabilities

| Capability | Description |
|------------|-------------|
| Multi-Source Crawling | Searches LinkedIn, GitHub, Naukri, internal databases, portfolio sites |
| Semantic Search | Uses embeddings to find candidates matching JD semantics, not just keywords |
| De-duplication | Identifies same candidate across multiple sources and merges profiles |
| Source Learning | Learns which sources yield the best candidates for which role types over time |
| Rate-Limit Awareness | Respects API limits, uses backoff strategies |

### Input
- Job description (structured requirements)
- Search preferences (sources to include/exclude)
- Previous search context (for re-ranking)

### Output
- List of candidate profiles with source metadata
- Confidence score per source
- Deduplication report

### Sources (Priority Order)
1. Internal company database / ATS
2. LinkedIn (API + scraping fallback)
3. GitHub (for technical roles)
4. Naukri.com / Indeed
5. Portfolio sites / personal websites
6. Open source contributions (for developer roles)

---

## 3. Matcher Agent

**Role:** The judge. Evaluates and ranks candidates based on holistic fit beyond keywords.

### Personality & Tone
Analytical, fair, explainable. Provides reasoning for every ranking decision.

### Core Capabilities

| Capability | Description |
|------------|-------------|
| Semantic Embedding | Converts JDs and candidate profiles into dense vector representations |
| Transferable Skill Detection | Identifies skills that transfer across domains (e.g., backend engineer -> AI engineer) |
| Behavioral Signal Analysis | Analyzes GitHub contribution patterns, open source activity, writing samples |
| Experience Weighting | Weighs relevant experience higher than total years |
| Explainable Ranking | Provides bullet-point reasoning for each candidate's score |
| Continuous Learning | Fine-tunes ranking based on recruiter feedback (which candidates were interviewed/hired) |

### Input
- Job description (embedding + structured fields)
- Candidate profiles from Sourcer Agent
- Historical hiring data (for learning)

### Output
- Ranked list of candidates with scores (0-100)
- Per-candidate explanation (strengths, gaps, why ranked)
- Skill gap analysis for each candidate

### Scoring Dimensions

| Dimension | Weight (configurable) | Description |
|-----------|----------------------|-------------|
| Skill Match | 40% | Direct and transferable skill overlap |
| Experience Relevance | 25% | Relevance of past roles and projects |
| Behavioral Signals | 15% | GitHub activity, writing samples, contributions |
| Education & Certifications | 10% | Degrees, courses, certifications |
| Career Trajectory | 10% | Growth rate, career progression quality |

---

## 4. Screener Agent

**Role:** The interviewer. Conducts voice-based preliminary assessments in the candidate's preferred language.

### Personality & Tone
Friendly, conversational, encouraging. Makes candidates comfortable. Adapts to their communication style.

### Core Capabilities

| Capability | Description |
|------------|-------------|
| Voice Conversation | Conducts natural, flowing voice calls (not rigid Q&A) |
| Multilingual Support | Speaks English, Hindi, Hinglish, and regional languages via Sarvam/Bhashini |
| Dynamic Questioning | Adapts questions based on candidate's responses (conversational tree) |
| Communication Assessment | Evaluates fluency, clarity, confidence, and articulation |
| Technical Sounding | Asks role-appropriate technical questions, evaluates problem-solving approach |
| Cultural Fit Assessment | Gauges values, work preferences, team collaboration style |
| Sentiment Analysis | Detects hesitation, enthusiasm, honesty indicators |

### Input
- Candidate profile (resume, experience, skills)
- Job description (required skills, seniority level)
- Interview parameters (duration, focus areas)

### Output
- Assessment report (communication score, technical score, cultural fit score)
- Full conversation transcript
- Key observations (strengths, concerns, recommendations)
- Recommendation: Proceed / Maybe / Reject

### Voice Pipeline

`
1. Orchestrator triggers Screener Agent for a candidate
2. Screener Agent sends calendar invite + prep email to candidate
3. At scheduled time, initiates voice call via Twilio/Vonage
4. Greets candidate, confirms identity, explains process
5. Begins with rapport-building questions
6. Transitions to role-specific questions (dynamic based on resume)
7. Asks behavioral questions (STAR format)
8. Opens floor for candidate questions
9. Closes with next steps
10. Generates assessment report and sends to Orchestrator
`

---

## 5. Scheduler Agent

**Role:** The coordinator. Manages interview scheduling, rescheduling, and reminders.

### Personality & Tone
Efficient, polite, precise. Respects everyone's time.

### Core Capabilities

| Capability | Description |
|------------|-------------|
| Calendar Integration | Reads/writes to Google Calendar, Outlook, iCal |
| Time Zone Awareness | Handles India's multiple time zones (IST across regions) |
| Availability Negotiation | Suggests optimal slots, negotiates with candidates via email/WhatsApp |
| Batch Scheduling | Books multiple interviews in optimal sequences (minimizing gaps) |
| Reminder System | Sends 24h and 1h reminders to both interviewer and candidate |
| Rescheduling Logic | Handles cancellations gracefully, finds next available slot |
| Feedback Collection | Sends post-interview feedback form to interviewer |

### Input
- List of shortlisted candidates
- Interviewer availability
- Interview duration and format (phone, video, in-person)

### Output
- Confirmed interview schedule
- Calendar events for all parties
- Reminder notifications schedule
- Daily schedule report for recruiter
