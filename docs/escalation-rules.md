# Escalation Rules — AI Recruiter Agent Swarm

---

## Philosophy

The system should be **autonomous by default, human-in-the-loop by exception**. Escalation happens only when the AI lacks sufficient confidence, encounters unresolvable conflicts, or when regulation/policy requires human judgment.

---

## Escalation Matrix

| Scenario | Trigger | Escalation Target | Severity | Auto-Resolvable? |
|----------|---------|-------------------|----------|-----------------|
| No candidates found after full search | Zero results from all sources | Recruiter | High | No — suggest JD changes |
| Low confidence across all candidates | Top candidate score < 60 | Recruiter | Medium | No — manual review needed |
| Tie between top candidates | Score difference < 1.0 | Recruiter | Low | Yes — flip a coin log |
| API rate limited repeatedly | 5 retry attempts exhausted | Admin | Medium | No — manual key rotation |
| Candidate complaint during screening | Candidate requests human | Recruiter | High | No — immediate intervention |
| Scheduling conflict unresolvable | 3 negotiation rounds fail | Recruiter | Low | Yes — manual override |
| PII / sensitive data detected | Credit card, Aadhaar in transcript | Security | Critical | Yes — auto-redact + notify |
| Recruiter feedback contradicts AI | Recruiter overrides ranking | Orchestrator | Info | Yes — update learning model |
| System confidence drop | Avg score drops 20% vs baseline | Engineering | High | No — investigate drift |
| Out-of-hours request | Recruiter action outside work hours | Orchestrator | Info | Yes — queue for next day |

---

## Escalation Flow

### Step 1: Internal Resolution Attempt

Before escalating, the agent tries automatic recovery:

```
1. DETECT issue
2. CLASSIFY severity
3. ATTEMPT auto-resolution (retry, alternative approach, degrade feature)
4. IF resolved -> log and continue
5. IF not resolved -> proceed to escalation
```

### Step 2: Escalation Message

```json
{
  "escalation_id": "esc_001",
  "correlation_id": "task_001",
  "timestamp": "2026-06-20T10:35:00Z",
  "severity": "high",
  "category": "no_candidates_found",
  "source_agent": "sourcer",
  "job_id": 1,
  "summary": "No candidates found matching the JD for Senior Full-Stack Developer across all 4 sources.",
  "details": {
    "sources_queried": ["linkedin", "github", "naukri", "internal_db"],
    "queries_attempted": ["Senior Full-Stack Developer", "Full-Stack Developer", "Full Stack Engineer"],
    "filters_applied": { "location": "Bengaluru", "experience": "3-7 years" },
    "retry_count": 5,
    "last_error": null
  },
  "suggested_actions": [
    "Expand location search to remote/pan-India",
    "Reduce experience requirement to 2-5 years",
    "Check if JD skills are too restrictive for the market",
    "Try sourcing from additional platforms (AngelList, Wellfound)"
  ],
  "context": {
    "jd_text": "We are looking for...",
    "required_skills": ["Python", "React", "Node.js", "AWS", "PostgreSQL"]
  }
}
```

### Step 3: Human Decision

The recruiter sees the escalation in the dashboard with:

1. **Problem summary** — what went wrong (one line)
2. **Suggested actions** — what the AI recommends
3. **Context** — JD, filters, what was tried
4. **Decision buttons**:
   - "Expand search" (relaxes filters and retries)
   - "Edit JD" (opens JD editor)
   - "Skip" (moves to next job)
   - "Manual mode" (switches to full manual control)

---

## Escalation Severity Levels

| Level | Response Time | Notify | Example |
|-------|---------------|--------|---------|
| **Critical** | Immediate | Recruiter + Admin + Email + SMS | PII leak, candidate distress |
| **High** | Within 1 hour | Recruiter + Dashboard alert | No candidates, all rejected |
| **Medium** | Within 4 hours | Recruiter + Dashboard | Low confidence, tie-breaking |
| **Low** | Within 24 hours | Dashboard only | Scheduling conflicts |
| **Info** | No action needed | Log entry | Feedback recorded |

---

## Auto-Resolutions (No Escalation)

These situations are handled automatically without bothering the recruiter:

| Situation | Auto-Resolution |
|-----------|----------------|
| LinkedIn API rate limited | Switch to GitHub + Naukri, retry LinkedIn in 30 min |
| Candidate doesn't answer call | Reschedule via WhatsApp, try 3 times |
| Calendar API down | Send manual email with proposed slots |
| Embedding model slow | Fall back to keyword matching temporarily |
| Voice transcript low confidence | Flag specific questions for human review, but proceed |
| Duplicate candidate found | Merge profiles, keep highest confidence source |

---

## Escalation Feedback Loop

Every escalation is recorded and used to improve the system:

- Which escalations were avoidable?
- Did the suggested actions help?
- What pattern led to the escalation?
- Update agent logic to prevent recurrence.

```json
{
  "escalation_id": "esc_001",
  "resolved": true,
  "resolution": "recruiter_expanded_location",
  "recruiter_feedback": "Expanded to remote. Found 23 candidates.",
  "outcome": "successful",
  "lesson": "Senior roles in Bengaluru have tight supply. Default to pan-India for senior roles.",
  "system_update": "Sourcer agent: for senior roles (5+ yr), automatically expand to remote if < 10 candidates found in first pass."
}
```
