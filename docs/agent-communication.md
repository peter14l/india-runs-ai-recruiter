# Agent Communication Protocol — AI Recruiter Agent Swarm

---

## Communication Model

Agents communicate **asynchronously** via a message broker (Redis PubSub / RabbitMQ). The Orchestrator manages the flow by sending tasks to agents and receiving results. Agents never communicate directly with each other — all inter-agent data flows through the Orchestrator.

This design ensures:
- **Observability** — every message is logged
- **Retry resilience** — failed messages can be re-queued
- **Scalability** — agents can be horizontally scaled independently
- **Audit trail** — complete history of all decisions

---

## Message Format

All agent-to-agent messages follow a standard envelope:

```json
{
  "message_id": "msg_abc123",
  "correlation_id": "task_xyz789",
  "type": "request | response | event | error",
  "source": "orchestrator | sourcer | matcher | screener | scheduler",
  "target": "orchestrator | sourcer | matcher | screener | scheduler",
  "timestamp": "2026-06-20T10:30:00Z",
  "payload": { },
  "metadata": {
    "retry_count": 0,
    "priority": "high | normal | low",
    "ttl_seconds": 3600
  }
}
```

---

## Task: Candidate Discovery

### 1. Orchestrator -> Sourcer: Search Request

**Type:** Request  
**Channel:** `agent:sourcer:search`

```json
{
  "message_id": "msg_001",
  "correlation_id": "task_001",
  "type": "request",
  "source": "orchestrator",
  "target": "sourcer",
  "timestamp": "2026-06-20T10:30:00Z",
  "payload": {
    "action": "search_candidates",
    "job_description": {
      "job_id": 1,
      "title": "Senior Full-Stack Developer",
      "required_skills": ["Python", "React", "Node.js", "AWS", "PostgreSQL"],
      "preferred_skills": ["Kubernetes", "TypeScript", "GraphQL"],
      "experience_min": 3,
      "experience_max": 7,
      "location": "Bengaluru",
      "jd_text": "We are looking for a Senior Full-Stack Developer...",
      "jd_embedding": [0.123, -0.456, ...]
    },
    "sources": ["linkedin", "github", "naukri", "internal_db"],
    "max_results": 100,
    "min_confidence": 0.6
  },
  "metadata": {
    "priority": "high",
    "ttl_seconds": 600
  }
}
```

### 2. Sourcer -> Orchestrator: Search Response

**Type:** Event  
**Channel:** `agent:orchestrator:sourcer_result`

```json
{
  "message_id": "msg_002",
  "correlation_id": "task_001",
  "type": "event",
  "source": "sourcer",
  "target": "orchestrator",
  "timestamp": "2026-06-20T10:32:30Z",
  "payload": {
    "action": "search_candidates",
    "status": "completed",
    "candidates": [
      {
        "candidate_id": "cand_001",
        "name": "Anand Kumar",
        "current_title": "Full-Stack Developer at TechCorp",
        "source": "linkedin",
        "source_url": "https://linkedin.com/in/anand-kumar",
        "confidence": 0.94,
        "extracted_skills": ["Python", "React", "Node.js", "AWS", "Docker"],
        "experience_years": 4,
        "location": "Bengaluru",
        "profile_summary": "Full-stack developer with experience in...",
        "resume_url": "https://storage.internal/resume_001.pdf"
      }
    ],
    "total_found": 45,
    "sources_used": ["linkedin", "github", "naukri"],
    "sources_failed": [],
    "execution_time_ms": 145000
  }
}
```

### 3. Sourcer -> Orchestrator: Progress Update

**Type:** Event  
**Channel:** `agent:orchestrator:progress`

```json
{
  "message_id": "msg_003",
  "correlation_id": "task_001",
  "type": "event",
  "source": "sourcer",
  "target": "orchestrator",
  "timestamp": "2026-06-20T10:31:00Z",
  "payload": {
    "action": "search_candidates",
    "progress": 0.45,
    "message": "Searching LinkedIn... 20 profiles found so far",
    "sources_completed": ["linkedin"],
    "sources_in_progress": ["github"],
    "sources_pending": ["naukri", "internal_db"]
  }
}
```

---

## Task: Candidate Ranking

### 4. Orchestrator -> Matcher: Ranking Request

```json
{
  "message_id": "msg_004",
  "correlation_id": "task_001",
  "type": "request",
  "source": "orchestrator",
  "target": "matcher",
  "timestamp": "2026-06-20T10:32:35Z",
  "payload": {
    "action": "rank_candidates",
    "job": {
      "job_id": 1,
      "title": "Senior Full-Stack Developer",
      "required_skills": ["Python", "React", "Node.js", "AWS", "PostgreSQL"],
      "preferred_skills": ["Kubernetes", "TypeScript", "GraphQL"],
      "jd_embedding": [0.123, -0.456, ...]
    },
    "candidates": [ ... ],
    "scoring_config": {
      "skill_match_weight": 0.40,
      "experience_weight": 0.25,
      "behavioral_weight": 0.15,
      "education_weight": 0.10,
      "trajectory_weight": 0.10,
      "transferable_skill_boost": 0.10
    }
  },
  "metadata": {
    "priority": "high",
    "ttl_seconds": 300
  }
}
```

### 5. Matcher -> Orchestrator: Ranking Response

```json
{
  "message_id": "msg_005",
  "correlation_id": "task_001",
  "type": "event",
  "source": "matcher",
  "target": "orchestrator",
  "timestamp": "2026-06-20T10:33:15Z",
  "payload": {
    "action": "rank_candidates",
    "status": "completed",
    "ranked_candidates": [
      {
        "candidate_id": "cand_001",
        "rank": 1,
        "composite_score": 94.2,
        "dimension_scores": {
          "skill_match": 38.0,
          "experience": 23.5,
          "behavioral": 14.0,
          "education": 9.0,
          "trajectory": 9.7
        },
        "explanation": "Strong match on core skills. Hands-on experience with Python, React, and AWS in production. Active GitHub contributor. Career progression shows increasing responsibility.",
        "skill_gaps": ["Kubernetes (preferred)"],
        "transferable_skills_detected": ["Led 2-person team — management potential"],
        "recommendation": "strong_proceed"
      }
    ],
    "distribution_stats": {
      "mean_score": 62.3,
      "median_score": 64.0,
      "std_dev": 18.7,
      "threshold_applied": 70.0,
      "above_threshold": 12
    },
    "execution_time_ms": 32000
  }
}
```

---

## Task: Candidate Screening

### 6. Orchestrator -> Screener: Screening Request

```json
{
  "message_id": "msg_006",
  "correlation_id": "task_001",
  "type": "request",
  "source": "orchestrator",
  "target": "screener",
  "timestamp": "2026-06-20T10:33:20Z",
  "payload": {
    "action": "screen_candidate",
    "candidate": {
      "candidate_id": "cand_001",
      "name": "Anand Kumar",
      "phone": "+91-98765XXXXX",
      "email": "anand@email.com",
      "preferred_language": "hinglish",
      "resume_text": "..."
    },
    "job": {
      "job_id": 1,
      "title": "Senior Full-Stack Developer",
      "required_skills": ["Python", "React", "Node.js", "AWS", "PostgreSQL"],
      "jd_text": "..."
    },
    "interview_config": {
      "max_duration_minutes": 15,
      "focus_areas": ["technical_depth", "communication", "cultural_fit"],
      "difficulty": "mid-senior"
    }
  },
  "metadata": {
    "priority": "normal",
    "ttl_seconds": 86400
  }
}
```

### 7. Screener -> Orchestrator: Progress Update (Call Scheduled)

```json
{
  "message_id": "msg_007",
  "correlation_id": "task_001",
  "type": "event",
  "source": "screener",
  "target": "orchestrator",
  "timestamp": "2026-06-20T10:35:00Z",
  "payload": {
    "action": "screen_candidate",
    "candidate_id": "cand_001",
    "status": "scheduled",
    "scheduled_time": "2026-06-21T11:00:00Z",
    "channel": "phone_call",
    "candidate_confirmed": true
  }
}
```

### 8. Screener -> Orchestrator: Assessment Result

```json
{
  "message_id": "msg_008",
  "correlation_id": "task_001",
  "type": "event",
  "source": "screener",
  "target": "orchestrator",
  "timestamp": "2026-06-21T11:15:00Z",
  "payload": {
    "action": "screen_candidate",
    "candidate_id": "cand_001",
    "status": "completed",
    "assessment": {
      "communication_score": 88,
      "technical_score": 92,
      "cultural_fit_score": 85,
      "overall_score": 88.3,
      "recommendation": "strong_proceed",
      "transcript_url": "https://storage.internal/transcripts/cand_001.json",
      "audio_recording_url": "https://storage.internal/recordings/cand_001.mp3",
      "duration_seconds": 612,
      "language_used": "hinglish"
    },
    "key_observations": [
      "Demonstrated strong understanding of microservices architecture",
      "Mentioned experience with migration project not listed on resume",
      "Good communication in Hinglish — switched naturally between Hindi and English",
      "Showed enthusiasm for the role and company mission"
    ],
    "red_flags": [],
    "custom_questions_asked": [
      "Can you describe a complex technical problem you solved?",
      "How do you approach debugging a production issue?",
      "Tell me about a time you disagreed with a team decision"
    ],
    "execution_time_ms": 612000
  }
}
```

---

## Task: Interview Scheduling

### 9. Orchestrator -> Scheduler: Scheduling Request

```json
{
  "message_id": "msg_009",
  "correlation_id": "task_001",
  "type": "request",
  "source": "orchestrator",
  "target": "scheduler",
  "timestamp": "2026-06-21T11:15:05Z",
  "payload": {
    "action": "schedule_interviews",
    "candidates": [
      {
        "candidate_id": "cand_001",
        "name": "Anand Kumar",
        "email": "anand@email.com",
        "phone": "+91-98765XXXXX",
        "timezone": "Asia/Kolkata"
      }
    ],
    "recruiters": [
      {
        "recruiter_id": "rec_001",
        "name": "Priya Sharma",
        "email": "priya@company.com",
        "calendar_provider": "google",
        "calendar_id": "priya@company.com",
        "working_hours": { "start": "09:00", "end": "18:00" },
        "buffer_minutes": 15
      }
    ],
    "preferences": {
      "interview_duration_minutes": 45,
      "earliest_date": "2026-06-23",
      "latest_date": "2026-06-27",
      "interview_type": "video_call",
      "auto_confirm": false
    }
  },
  "metadata": {
    "priority": "normal",
    "ttl_seconds": 172800
  }
}
```

### 10. Scheduler -> Orchestrator: Scheduling Response

```json
{
  "message_id": "msg_010",
  "correlation_id": "task_001",
  "type": "event",
  "source": "scheduler",
  "target": "orchestrator",
  "timestamp": "2026-06-21T11:20:00Z",
  "payload": {
    "action": "schedule_interviews",
    "status": "pending_confirmation",
    "proposed_slots": [
      {
        "candidate_id": "cand_001",
        "recruiter_id": "rec_001",
        "slot": "2026-06-23T10:00:00Z",
        "duration_minutes": 45,
        "candidate_notified": true,
        "recruiter_notified": true,
        "candidate_response": "pending",
        "meeting_link": "https://meet.google.com/abc-defg-hij"
      },
      {
        "candidate_id": "cand_001",
        "recruiter_id": "rec_001",
        "slot": "2026-06-24T14:00:00Z",
        "duration_minutes": 45,
        "candidate_notified": true,
        "recruiter_notified": true,
        "candidate_response": "pending",
        "meeting_link": "https://meet.google.com/klm-nopq-rst"
      }
    ],
    "execution_time_ms": 4500
  }
}
```

---

## Error Handling

### Message Retry Protocol

| Attempt | Delay | Action |
|---------|-------|--------|
| 1 | 5s | Retry |
| 2 | 30s | Retry |
| 3 | 120s | Retry |
| 4 | 300s | Retry with degraded config |
| 5 | - | Mark as failed, escalate |

### Error Message Format

```json
{
  "message_id": "msg_err_001",
  "correlation_id": "task_001",
  "type": "error",
  "source": "sourcer",
  "target": "orchestrator",
  "timestamp": "2026-06-20T10:31:30Z",
  "payload": {
    "action": "search_candidates",
    "error_code": "API_RATE_LIMITED",
    "error_message": "LinkedIn API rate limit exceeded. Reset at: 2026-06-20T11:00:00Z",
    "retry_count": 3,
    "retry_allowed": true,
    "suggested_action": "RETRY_AFTER_BACKOFF",
    "source": "linkedin"
  }
}
```

---

## Channel Map

| Channel | Direction | Purpose |
|---------|-----------|---------|
| `agent:orchestrator:commands` | -> Orchestrator | External commands (UI, API) |
| `agent:sourcer:search` | -> Sourcer | Trigger candidate search |
| `agent:matcher:rank` | -> Matcher | Trigger candidate ranking |
| `agent:screener:screen` | -> Screener | Trigger candidate screening |
| `agent:scheduler:schedule` | -> Scheduler | Trigger interview scheduling |
| `agent:orchestrator:results` | -> Orchestrator | All agents return results here |
| `agent:orchestrator:progress` | -> Orchestrator | Real-time progress updates |
| `agent:orchestrator:errors` | -> Orchestrator | Error notifications |
| `agent:orchestrator:escalations` | -> Orchestrator | Human escalation requests |
