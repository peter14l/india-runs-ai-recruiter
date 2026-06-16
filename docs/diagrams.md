# Diagrams — AI Recruiter Agent Swarm

All diagrams are written in Mermaid format. Render them using any Mermaid-compatible viewer (GitHub renders these natively).

---

## 1. System Architecture Diagram

```mermaid
graph TB
    subgraph "User Layer"
        UI[Recruiter Dashboard]
        API[External API]
    end

    subgraph "Orchestration Layer"
        ORC[Orchestrator Agent]
        SM[State Manager]
        HR[Human Escalation Handler]
    end

    subgraph "Agent Layer"
        SA[Sourcer Agent]
        MA[Matcher Agent]
        SCA[Screener Agent]
        SCHA[Scheduler Agent]
    end

    subgraph "Memory & Context Layer"
        VDB[(Vector DB\nQdrant)]
        KV[(Cache\nRedis)]
        SQL[(Relational DB\nPostgreSQL)]
        KG[Knowledge Graph]
    end

    subgraph "Integration Layer"
        LI[LinkedIn API]
        GH[GitHub API]
        NK[Naukri API]
        CL[Calendar API]
        EM[Email/WhatsApp]
        TL[Telephony\nTwilio]
    end

    UI --> ORC
    API --> ORC
    ORC --> SM
    ORC --> HR
    ORC --> SA
    ORC --> MA
    ORC --> SCA
    ORC --> SCHA
    SA --> LI
    SA --> GH
    SA --> NK
    MA --> VDB
    SCA --> TL
    SCHA --> CL
    SCHA --> EM
    SA --> VDB
    MA --> SQL
    SCA --> SQL
    SCHA --> SQL
    ORC --> KV
    ORC --> KG
```

---

## 2. Agent Communication Sequence (Normal Flow)

```mermaid
sequenceDiagram
    participant R as Recruiter
    participant O as Orchestrator
    participant S as Sourcer
    participant M as Matcher
    participant SC as Screener
    participant SCH as Scheduler

    R->>O: Submit Job Description
    O->>O: Parse & validate JD
    O->>S: search_candidates(jd, sources)
    S->>S: Crawl LinkedIn, GitHub, Naukri
    S-->>O: candidates_found(profiles)

    O->>M: rank_candidates(jd, profiles)
    M->>M: Embed JD + profiles
    M->>M: Compute scores
    M-->>O: ranked_shortlist(ranked_list)

    O->>O: Select top N candidates
    O->>SC: screen_candidate(candidate, jd)
    SC->>SC: Generate questions
    SC->>SC: Conduct voice call
    SC-->>O: assessment_report

    O->>SCH: schedule_interviews(candidates, recruiters)
    SCH->>SCH: Check availability
    SCH->>SCH: Send invitations
    SCH-->>O: confirmed_schedule

    O->>O: Compile final output
    O-->>R: final_shortlist(summary)
```

---

## 3. Orchestrator State Machine

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> ParsingJD: New JD received
    ParsingJD --> Sourcing: JD parsed successfully
    ParsingJD --> Error: Invalid JD format
    Error --> Idle: Retry / Human fix

    Sourcing --> Matching: Candidates found
    Sourcing --> SourcingRetry: Partial results
    Sourcing --> Escalation: No candidates found
    SourcingRetry --> Matching: Retry successful
    SourcingRetry --> Escalation: All sources exhausted

    Matching --> Screening: Top candidates identified
    Matching --> Escalation: No qualified candidates
    Matching --> MatchingRetry: Low confidence scores
    MatchingRetry --> Screening: Retry with adjusted weights

    Screening --> Scheduling: Assessments complete
    Screening --> Escalation: All candidates rejected

    Scheduling --> Compiling: Schedule confirmed
    Scheduling --> Escalation: Scheduling conflicts

    Compiling --> Reviewing: Final shortlist ready
    Reviewing --> Idle: Recruiter approves
    Reviewing --> FeedbackLoop: Recruiter provides feedback
    FeedbackLoop --> Idle: Feedback incorporated

    Escalation --> Idle: Human decision made
```

---

## 4. Sourcer Agent Flow

```mermaid
flowchart LR
    A[Receive JD] --> B{Check Cache}
    B -->|Cache Hit| C[Return cached results]
    B -->|Cache Miss| D[Parse sources list]
    D --> E[Select source]
    E --> F{Has API?}
    F -->|Yes| G[Query API]
    F -->|No| H[Fallback scrape]
    G --> I[Parse results]
    H --> I
    I --> J{More sources?}
    J -->|Yes| E
    J -->|No| K[Deduplicate]
    K --> L[Merge profiles]
    L --> M[Rank by confidence]
    M --> N[Cache results]
    N --> O[Return to Orchestrator]
```

---

## 5. Matcher Agent Scoring Pipeline

```mermaid
flowchart TD
    A[JD + Candidate Profiles] --> B[Generate Embeddings]
    B --> C[Compute Similarity Scores]
    
    subgraph Scoring Dimensions
        D1[Skill Match\nWeight: 40%]
        D2[Experience\nWeight: 25%]
        D3[Behavioral\nWeight: 15%]
        D4[Education\nWeight: 10%]
        D5[Trajectory\nWeight: 10%]
    end
    
    C --> D1
    C --> D2
    C --> D3
    C --> D4
    C --> D5
    
    D1 --> E[Weighted Aggregation]
    D2 --> E
    D3 --> E
    D4 --> E
    D5 --> E
    
    E --> F[Composite Score 0-100]
    F --> G{Score > Threshold?}
    G -->|Yes| H[Include in shortlist]
    G -->|No| I[Exclude with reason]
    H --> J[Generate Explanation]
    I --> J
    J --> K[Return Ranked List]
```

---

## 6. Screener Agent Voice Pipeline

```mermaid
sequenceDiagram
    participant O as Orchestrator
    participant S as Screener Agent
    participant T as Telephony API
    participant C as Candidate
    participant AS as Assessment Engine

    O->>S: screen_candidate(profile, jd)
    S->>S: Generate personalized questions
    S->>C: Send invitation (WhatsApp)
    C-->>S: Accept invite
    S->>T: Initiate call
    T->>C: Ring
    C->>T: Answer
    Note over S,C: Conversation begins
    
    loop Q&A Cycle
        S->>T: Speak question
        T->>C: Audio
        C->>T: Response
        T->>S: Transcribe audio
        S->>AS: Evaluate response
    end
    
    C->>T: Hang up
    T->>S: Call ended
    S->>AS: Compile assessment
    AS-->>S: scores + transcript
    S-->>O: assessment_report
```

---

## 7. Human Escalation Decision Tree

```mermaid
flowchart TD
    A[Agent encounters issue] --> B{Issue Type?}
    
    B -->|No candidates found| C[Increase source scope]
    C --> D{Still empty?}
    D -->|Yes| E[Escalate to Recruiter\nSuggest JD expansion]
    D -->|No| F[Continue normal flow]
    
    B -->|Low confidence scores| G[Adjust scoring weights]
    G --> H{Still low?}
    H -->|Yes| I[Escalate to Recruiter\nFlag for manual review]
    H -->|No| F
    
    B -->|All candidates rejected| J[Log rejection reasons]
    J --> K[Escalate to Recruiter\nSuggest JD revisions]
    
    B -->|Scheduling conflict| L[Try alternatives]
    L --> M{Resolved?}
    M -->|No| N[Escalate to Recruiter\nManual scheduling]
    M -->|Yes| F
    
    B -->|API rate limited| O[Backoff & retry]
    O --> P{Retries exhausted?}
    P -->|Yes| Q[Escalate to Recruiter\nManual sourcing required]
    P -->|No| F
    
    B -->|Candidate complaint| R[Pause screening]
    R --> S[Escalate to Recruiter\nHuman intervention needed]
```
