"""
Matcher Agent — Evaluates and ranks candidates holistically.

Responsible for:
  - Embedding job descriptions and candidate profiles into vector space
  - Computing semantic similarity beyond keyword matching
  - Scoring candidates across 5 weighted dimensions
  - Detecting transferable skills (e.g., backend -> AI)
  - Generating human-readable explanations for each ranking
  - Learning from recruiter feedback to improve future rankings

Scoring Dimensions:
  - Skill Match (40%): Direct + transferable skill overlap
  - Experience Relevance (25%): Relevance of past roles and projects
  - Behavioral Signals (15%): GitHub activity, writing samples, OSS contributions
  - Education & Certifications (10%): Degrees, courses, certifications
  - Career Trajectory (10%): Growth rate, promotion history, responsibility increase
"""


class MatcherAgent:
    def __init__(self, embedding_model, vector_db, scoring_config=None):
        self.embedding_model = embedding_model
        self.vector_db = vector_db
        self.scoring_config = scoring_config or self._default_scoring_config()

    def rank(self, jd: dict, candidates: list) -> dict:
        """Rank candidates against job. Returns ordered list with scores + explanations."""

    def _compute_skill_match(self, jd_skills: list, candidate_skills: list) -> tuple:
        """Compute direct match + transferable skill score. Returns (score, details)."""

    def _detect_transferable_skills(self, candidate_history: list) -> list:
        """Identify skills that transfer across domains/roles."""

    def _compute_experience_relevance(self, jd: dict, candidate: dict) -> float:
        """Evaluate how relevant past experience is to this role."""

    def _compute_behavioral_signals(self, candidate: dict) -> float:
        """Score based on GitHub activity, blog posts, OSS contributions."""

    def _compute_education_score(self, jd: dict, candidate: dict) -> float:
        """Score education relevance."""

    def _compute_trajectory_score(self, candidate: dict) -> float:
        """Score career progression quality."""

    def _aggregate_scores(self, dimension_scores: dict) -> float:
        """Weighted aggregation of all dimension scores."""

    def _generate_explanation(self, candidate: dict, scores: dict) -> str:
        """Generate human-readable ranking explanation."""

    @staticmethod
    def _default_scoring_config() -> dict:
        return {
            "skill_match_weight": 0.40,
            "experience_weight": 0.25,
            "behavioral_weight": 0.15,
            "education_weight": 0.10,
            "trajectory_weight": 0.10,
        }
