"""
State Manager — Tracks the state of every recruitment pipeline.

Uses Redis for real-time state (fast, ephemeral) and PostgreSQL for
persistent storage and audit trail.

Pipeline States:
  - created: JD received, not yet processed
  - parsing: JD being analyzed
  - sourcing: Sourcer Agent active
  - matching: Matcher Agent active
  - screening: Screener Agent active
  - scheduling: Scheduler Agent active
  - compiling: Orchestrator aggregating results
  - review_ready: Awaiting recruiter review
  - completed: Recruiter approved/dismissed
  - escalated: Human intervention needed
  - failed: Irrecoverable error
"""


class StateManager:
    def __init__(self, redis_client, db_client):
        self.redis = redis_client
        self.db = db_client

    def create_pipeline(self, job_id: str, jd: dict) -> str:
        """Initialize a new pipeline with initial state."""

    def get_state(self, job_id: str) -> dict:
        """Get current state of a pipeline."""

    def update_state(self, job_id: str, new_state: str, metadata: dict = None) -> bool:
        """Transition pipeline to new state."""

    def append_log(self, job_id: str, agent: str, action: str, details: dict) -> None:
        """Add an audit log entry for the pipeline."""

    def get_pipeline_history(self, job_id: str) -> list:
        """Get full history of state transitions for a pipeline."""

    def list_active_pipelines(self, recruiter_id: str = None) -> list:
        """List all currently active pipelines."""

    def get_stats(self) -> dict:
        """Return aggregate pipeline statistics."""
