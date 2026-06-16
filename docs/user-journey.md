# User Journey — AI Recruiter Agent Swarm

---

## Persona: Priya, HR Manager at a Bengaluru-based tech company

**Background:** Priya manages hiring for her 200-person company. She receives 500+ applications per role. Currently spends 60% of her time screening resumes and scheduling calls. She has tried AI tools but found them to be black boxes — they reject candidates without explanation.

**Goal:** Find the best candidates faster, with transparency into why each candidate was selected.

---

## Step-by-Step Journey

### Step 1: Submitting a Job Opening

**Priya's action:** Logs into the dashboard, pastes the job description for "Senior Full-Stack Developer", sets preferences (auto-screen: yes, auto-schedule: no, top 10 candidates for manual review).

**System reaction:** Orchestrator Agent parses the JD, extracts 12 required skills, 5 preferred skills, 3-5 years experience, Bengaluru location. Creates a new job entry in the database.

**Priya feels:** Quick, familiar, no learning curve. "This feels like posting a job anywhere else."

---

### Step 2: Watching the Swarm Work (Dashboard)

**Priya's action:** Opens the job dashboard, sees live status:

`
Job: Senior Full-Stack Developer
Status: Processing
Agents at work:
  - Sourcer: Searching 4 sources... (12 profiles found)
  - Matcher: Ranking candidates...
  - Screener: Ready (waiting for ranked shortlist)
  - Scheduler: Idle
Estimated time remaining: 4 minutes
`

**System reaction:** Real-time streaming of agent progress via WebSocket.

**Priya feels:** Impressed by the transparency. "I can see exactly what's happening. No black box."

---

### Step 3: Reviewing the Ranked Shortlist

**Priya's action:** 5 minutes later, sees a ranked list of 25 candidates. Each has a match score, an explanation, and a breakdown.

**System reaction:** Matcher Agent outputs scoring breakdown per candidate:

`
Rank 1: Anand Kumar - 94/100
  Skills: 38/40 (Python, React, Node.js, AWS, Docker)
  Experience: 23/25 (4 years, relevant projects)
  Signals: 14/15 (Active GitHub, blog writer)
  Education: 8/10 (B.Tech CS, NIT)
  Trajectory: 11/10 (promoted twice in 3 years)

Key strengths: End-to-end project ownership
Skill gaps: Kubernetes (preferred, not required)
Transferable skills: Led 2-person team (management potential)
`

**Priya feels:** Confident. The explanations help her trust the rankings. "I can see *why* Anand is ranked first, not just that he is."

---

### Step 4: Voice Screening (Automatic)

**Priya's action:** Does nothing — the Screener Agent takes over automatically.

**System reaction:**
1. Screener Agent sends Anand a WhatsApp message: "Hi Anand! I'm the AI screener for the Senior Full-Stack role at TechCorp. Can we chat for 10 minutes tomorrow at 11 AM?"
2. Anand confirms.
3. At 11 AM, AI calls Anand's phone. Conversation flows naturally in Hinglish.
4. After 10 minutes, assessment is generated:

`
Communication: 88/100 (clear, confident)
Technical: 92/100 (answered all questions correctly)
Cultural fit: 85/100 (values alignment, team orientation)
Recommendation: STRONG PROCEED

Notable: Candidate mentioned experience with microservices migration
          that wasn't on resume. Flagged for human review.
`

**Priya feels:** Surprised at the quality. "It picked up on something his resume didn't mention. No human screener would have caught that."

---

### Step 5: Manual Review & Decision

**Priya's action:** Reviews the top 5 candidates manually. Reads the assessment reports. Flags 2 candidates for the next round. One-click schedules interviews with her team.

**System reaction:** Scheduler Agent checks team calendars, proposes slots, sends invites. Priya just clicks "Approve".

**Priya feels:** In control. "The AI did the heavy lifting, but I made the final call. Perfect balance."

---

### Step 6: Feedback Loop

**Priya's action:** After interviews, rates each candidate (1-5) and marks hired/rejected with brief notes.

**System reaction:** Feedback is stored and used to fine-tune the Matcher Agent's scoring weights. Next time Priya posts a similar role, the rankings will be even better.

**Priya feels:** Growing trust. "The system is learning from my decisions. It gets better every time."

---

## Journey Map (Visual)

`
POST JOB  -->  SWARM PROCESSES  -->  REVIEW  -->  DECIDE  -->  LEARN
   |              |                    |            |            |
   v              v                    v            v            v
 Paste JD    See agent cards     Read ranked     Select      Feedback
 Set prefs   Live progress      list with       top 5       improves
 Click save  notification       explanations    Schedule    next search
                                Listen to        interviewed
                                screening
                                recordings
`

---

## Pain Points Solved

| Before (Traditional ATS) | After (This System) |
|--------------------------|---------------------|
| Priya reviews 500+ resumes manually | AI ranks 500 into top 25 with explanations |
| 60% time on screening | 10% time on review, 90% on high-value decisions |
| Black-box AI rejects without reason | Transparent scoring with reasoning |
| Only English resumes considered | Voice screening in Hinglish/regional languages |
| Scheduling takes 5-7 email exchanges | AI schedules in one click |
| No learning from past decisions | System improves with every hire |
