# AI Recruiter — Track 1: Data & AI Challenge

> **India Runs Hackathon 2026** by Redrob AI  
> Candidate ranking system for Senior AI Engineer — Founding Team at Redrob AI.

## Overview

Multi-dimensional scoring system that ranks 100K+ candidate profiles from `candidates.jsonl` against a job description. Uses TF-IDF semantic similarity, skill matching, experience fit, title relevance, Redrob behavioral signals, location, and education — with honeypot anomaly detection.

**Top candidates produced (actual AI/ML engineers):**
- Rank 1: Senior ML Engineer, 7.2yrs, 10/10 AI skills, Pune
- Rank 2: Senior Data Scientist, 5.2yrs, 10/10 AI skills, responsive
- Rank 3: Senior ML Engineer, 6.1yrs, 10/10 AI skills, Bangalore

## Reproduce

```bash
pip install -r requirements.txt
python matcher.py --candidates ./candidates.jsonl --out ./output/peter14l.csv
```

Expected runtime: **~2 minutes** for 100K candidates on an 8-core CPU.  
Output: `output/peter14l.csv` (top 100 ranked candidates with scores and reasoning).

## Scoring Dimensions

| Component | Weight | Description |
|-----------|--------|-------------|
| AI Skills Match | 25% | 39 JD-specific AI/ML skills matched against candidate skills + profile text |
| JD Similarity | 25% | TF-IDF cosine similarity between JD and candidate profile |
| Experience Fit | 15% | Gaussian decay around ideal 5–9 year range |
| Title Relevance | 12% | Current title/headline keyword match for AI/ML roles |
| Redrob Signals | 10% | Response rate, profile completeness, GitHub activity, recruiter saves |
| Location | 8% | Pune/Noida (1.0), other Indian cities (0.85), India remote (0.45–0.6) |
| Education | 5% | CS/AI/ML fields (1.0), tier-1 + advanced degree bonus |
| Honeypot Penalty | — | Up to −0.30 for impossible career durations or skill/experience mismatch |

## Project Structure

```
track1/
├── matcher.py                 # Ranking pipeline (entry point)
├── requirements.txt           # Dependencies
├── submission_metadata.yaml   # Portal metadata mirror
├── README.md                  # This file
└── output/
    └── peter14l.csv           # Generated submission (top 100)
```

## Validation

Use the official validator from the hackathon bundle:

```bash
python validate_submission.py output/peter14l.csv
```

## Notes

- **CPU-only, no network**: Runs entirely offline on a single CPU core.
- **No LLM calls during ranking**: TF-IDF + rule-based scoring only.
- **Honeypot detection**: Checks for claimed experience exceeding possible career duration and skills/experience ratio anomalies.
- **Deterministic tie-breaking**: Equal scores ordered by `candidate_id` ascending.
