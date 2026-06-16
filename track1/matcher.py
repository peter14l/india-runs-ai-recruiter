"""
AI Recruiter — Intelligent Candidate Ranking System
Track 1: Data & AI Challenge — India Runs by Redrob AI

Multi-dimensional scoring for Senior AI Engineer at Redrob AI.
Usage: python matcher.py --candidates ./candidates.jsonl --out ./submission.csv
"""

import argparse
import json
import csv
import re
import time
from pathlib import Path

import docx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


TOP_N = 100


# ─── 1. JD Loading ──────────────────────────────────────────────────────────
def load_jd(path):
    doc = docx.Document(str(path))
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

def extract_jd_reqs(text):
    low = text.lower()

    ai_skills = [
        "embeddings", "sentence-transformers", "bge", "e5", "openai embeddings",
        "vector database", "qdrant", "pinecone", "weaviate", "milvus", "faiss",
        "hybrid search", "retrieval", "ranking",
        "llm", "fine-tuning", "lora", "peft",
        "ndcg", "mrr", "map", "learning-to-rank", "evaluation framework",
        "python", "production",
        "bert", "transformer", "xgboost",
        "docker", "kubernetes", "fastapi",
        "elasticsearch", "opensearch",
        "airflow", "kafka", "spark",
        "sql", "redis", "postgresql",
    ]

    exp_m = re.search(r'(\d+)[–\-]\s*(\d+)\s*years', low)
    exp_range = (int(exp_m.group(1)), int(exp_m.group(2))) if exp_m else (5, 9)

    target_cities = ["pune", "noida", "mumbai", "bangalore", "bengaluru",
                     "delhi", "gurgaon", "hyderabad", "chennai", "kolkata",
                     "gandhinagar", "ahmedabad", "indore", "jaipur", "coimbatore"]
    india_countries = {"india", "in"}

    return {
        "ai_skills": ai_skills,
        "exp_min": exp_range[0], "exp_max": exp_range[1],
        "exp_ideal_min": 5, "exp_ideal_max": 9,
        "target_cities": target_cities,
        "india_countries": india_countries,
        "text": text, "text_lower": low,
    }

# ─── 2. Candidate Loading ───────────────────────────────────────────────────
def load_jsonl(path, limit=None):
    cands = []
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if limit and i >= limit:
                break
            cands.append(json.loads(line))
    return cands

# ─── 3. Scoring Dimensions ──────────────────────────────────────────────────

# 3a. AI Skills Match (0-1)
def score_ai_skills(cand, reqs):
    skills = set(s["name"].lower().strip() for s in cand.get("skills", []))
    text = (cand.get("profile", {}).get("summary", "") + " " +
            " ".join(h.get("description", "") for h in cand.get("career_history", []))).lower()

    matched = sum(1 for s in reqs["ai_skills"] if s in skills or s in text)
    total = len(reqs["ai_skills"])
    return min(1.0, (matched / total) * 3.0)

# 3b. Ideal Experience (0-1)
def score_exp(years, reqs):
    if years is None:
        return 0.3
    lo, hi = reqs["exp_ideal_min"], reqs["exp_ideal_max"]
    if lo <= years <= hi:
        return 1.0
    if years < lo:
        return max(0.2, 1.0 - (lo - years) * 0.12)
    return max(0.15, 1.0 - (years - hi) * 0.06)

# 3c. Title Relevance (0-1)
def score_title(cand):
    t = ((cand.get("profile", {}).get("current_title", "") or "") + " " +
         (cand.get("profile", {}).get("headline", "") or "")).lower()
    for kw in ["ai engineer", "machine learning engineer", "ml engineer",
               "senior ai", "senior ml", "data scientist",
               "nlp", "deep learning", "llm"]:
        if kw in t:
            return 1.0
    for kw in ["data engineer", "backend engineer", "software engineer",
               "applied scientist", "mlops"]:
        if kw in t:
            return 0.7
    return 0.25

# 3d. Location (0-1)
def score_loc(cand, reqs):
    loc = (cand.get("profile", {}).get("location", "") or "").lower()
    country = (cand.get("profile", {}).get("country", "") or "").lower()
    willing = cand.get("redrob_signals", {}).get("willing_to_relocate", False)

    if "pune" in loc or "noida" in loc:
        return 1.0
    for c in reqs["target_cities"]:
        if c in loc:
            return 0.85
    if country in reqs["india_countries"]:
        return 0.6 if willing else 0.45
    return 0.25

    # 3e. Redrob Signals (0-1)
def score_signals(cand):
    s = cand.get("redrob_signals", {})
    if not s:
        return 0.3
    parts = [
        min(1.0, s.get("profile_completeness_score", 0) / 80),
        s.get("recruiter_response_rate", 0),
        min(1.0, s.get("saved_by_recruiters_30d", 0) / 10),
        min(1.0, max(0, s.get("github_activity_score", -1)) / 60) if s.get("github_activity_score", -1) >= 0 else 0.3,
        1.0 if s.get("open_to_work_flag") else 0.5,
        min(1.0, s.get("profile_views_received_30d", 0) / 50),
        min(1.0, s.get("search_appearance_30d", 0) / 30),
        s.get("interview_completion_rate", 0),
        min(1.0, s.get("connection_count", 0) / 500),
        (s.get("verified_email", False) + s.get("verified_phone", False)) / 2,
    ]
    return sum(parts) / len(parts)

# 3h. Honeypot penalty (profiles with impossible career histories)
def score_honeypot_penalty(cand):
    penalty = 0.0
    p = cand.get("profile", {})
    years = p.get("years_of_experience", 0)
    if not years:
        return 0.0

    career = cand.get("career_history", [])
    if not career:
        return 0.0

    earliest_year = 9999
    for h in career:
        start = h.get("start_date", "")
        if start and len(start) >= 4:
            try:
                y = int(start[:4])
                if y < earliest_year:
                    earliest_year = y
            except ValueError:
                pass

    current_year = 2026
    if earliest_year < 9999:
        max_possible = current_year - earliest_year
        if years > max_possible + 3:
            penalty += 0.15

    skill_count = len(cand.get("skills", []))
    if skill_count > 15 and years < 3:
        penalty += 0.10
    if skill_count > 25 and years < 5:
        penalty += 0.05

    return min(0.3, penalty)

# 3f. Education Relevance (0-1)
def score_edu(cand):
    best = 0.2
    for e in cand.get("education", []):
        field = (e.get("field_of_study", "") or "").lower()
        degree = (e.get("degree", "") or "").lower()
        tier = e.get("tier", "unknown")

        s = 0.3
        for hf in ["computer science", "artificial intelligence", "machine learning",
                    "data science", "mathematics", "statistics", "electrical engineering",
                    "information technology"]:
            if hf in field:
                s = 1.0
                break
        if s < 1.0:
            for mf in ["engineering", "physics", "economics"]:
                if mf in field:
                    s = 0.7
                    break

        if tier == "tier_1":
            s = min(1.0, s + 0.15)
        if any(d in degree for d in ["phd", "doctorate", "master", "m.tech"]):
            s = min(1.0, s + 0.1)
        best = max(best, s)
    return best

# 3g. JD Semantic Similarity
def score_jd_sim(cand, vec, jd_vec):
    text = " ".join([
        cand.get("profile", {}).get("summary", "") or "",
        cand.get("profile", {}).get("headline", "") or "",
        " ".join(h.get("description", "") for h in cand.get("career_history", [])),
    ])
    sim = cosine_similarity(vec.transform([text]), jd_vec)[0][0]
    return float(max(0, min(1, sim * 4)))

# ─── 4. Composite Score ─────────────────────────────────────────────────────
def compute_score(cand, reqs, vec, jd_vec):
    p = cand.get("profile", {})
    years = p.get("years_of_experience")

    sk = score_ai_skills(cand, reqs)
    ex = score_exp(years, reqs)
    ti = score_title(cand)
    lo = score_loc(cand, reqs)
    si = score_signals(cand)
    ed = score_edu(cand)
    jd = score_jd_sim(cand, vec, jd_vec)
    hp = score_honeypot_penalty(cand)

    weights = {"skills": 0.25, "exp": 0.15, "title": 0.12, "loc": 0.08,
               "signals": 0.10, "edu": 0.05, "jd_sim": 0.25}
    total = (sk * weights["skills"] + ex * weights["exp"] + ti * weights["title"] +
             lo * weights["loc"] + si * weights["signals"] + ed * weights["edu"] +
             jd * weights["jd_sim"]) - hp

    total = max(0.0, total)

    title = p.get("current_title", "Unknown")
    sig = cand.get("redrob_signals", {})
    loc = (p.get("location", "") or "").strip()
    parts = []
    parts.append(f"{title} with {years}yrs")
    if sk >= 0.8:
        parts.append("strong AI/ML skill alignment")
    parts.append(f"{loc}")
    if sig.get("recruiter_response_rate", 0) > 0.5:
        parts.append("responsive")
    if hp > 0:
        parts.append("(career history anomaly detected)")

    reasoning = "; ".join(parts)

    return round(total, 4), reasoning

# ─── 5. Pipeline ────────────────────────────────────────────────────────────
def run(candidates, label, reqs, vec, jd_vec):
    n = len(candidates)
    print(f"  Scoring {n} {label}...")
    results = []
    t0 = time.time()
    for i, cand in enumerate(candidates):
        cid = cand.get("candidate_id", f"CAND_{i:07d}")
        score, reasoning = compute_score(cand, reqs, vec, jd_vec)
        results.append((cid, score, reasoning))
        if (i+1) % max(1, n//20) == 0:
            elapsed = time.time() - t0
            rate = (i+1) / elapsed if elapsed > 0 else 0
            print(f"    [{i+1}/{n}] {rate:.0f}/sec", end="\r")
    elapsed = time.time() - t0
    print(f"    Done in {elapsed:.1f}s ({n/elapsed:.0f}/sec)")
    results.sort(key=lambda x: (-x[1], x[0]))
    return results

def write_output(results, path):
    n = min(TOP_N, len(results))
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["candidate_id", "rank", "score", "reasoning"])
        for rank, (cid, score, reasoning) in enumerate(results[:n], 1):
            writer.writerow([cid, rank, f"{score:.4f}", reasoning])
    print(f"  Wrote top {n} to {path}")

def main():
    parser = argparse.ArgumentParser(
        description="AI Recruiter — Track 1 Candidate Ranking System"
    )
    parser.add_argument("--candidates", required=True,
                        help="Path to candidates.jsonl")
    parser.add_argument("--jd", default=None,
                        help="Path to job_description.docx (uses default if not provided)")
    parser.add_argument("--out", default="submission.csv",
                        help="Output CSV path (default: submission.csv)")
    parser.add_argument("--limit", type=int, default=None,
                        help="Limit number of candidates (for testing)")
    args = parser.parse_args()

    DATA_DIR = Path(args.candidates).parent
    jd_path = Path(args.jd) if args.jd else DATA_DIR / "job_description.docx"

    OUTPUT_PATH = Path(args.out)

    print("=" * 60)
    print("AI Recruiter — Intelligent Candidate Ranking System")
    print("Track 1: Data & AI Challenge — India Runs 2026")
    print("=" * 60)

    print("\n[1] Loading JD...")
    jd_text = load_jd(jd_path)
    reqs = extract_jd_reqs(jd_text)
    print(f"  Role: {jd_text.split(chr(10))[0][:70]}")
    print(f"  Skills tracked: {len(reqs['ai_skills'])}")

    print("\n[2] Building TF-IDF...")
    vec = TfidfVectorizer(max_features=5000, stop_words="english",
                          ngram_range=(1,2), sublinear_tf=True)
    jd_vec = vec.fit_transform([jd_text])
    print(f"  Vocab: {len(vec.get_feature_names_out())}")

    print("\n[3] Loading candidates...")
    t0 = time.time()
    candidates = load_jsonl(args.candidates, limit=args.limit)
    print(f"  Loaded {len(candidates)} candidates in {time.time()-t0:.1f}s")

    print("\n[4] Scoring all candidates...")
    results = run(candidates, "candidates", reqs, vec, jd_vec)

    print("\n[5] Writing output...")
    write_output(results, OUTPUT_PATH)

    print("\n" + "=" * 60)
    print("TOP 20 RANKED CANDIDATES")
    print("=" * 60)
    print(f"{'Rank':<6}{'ID':<16}{'Score':<9}{'Reasoning'}")
    print("-" * 70)
    for rank, (cid, score, reasoning) in enumerate(results[:20], 1):
        print(f"{rank:<6}{cid:<16}{score:<9.4f}{reasoning[:60]}")

    print(f"\nDone! Output: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
