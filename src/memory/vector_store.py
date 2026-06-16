"""
Vector Store — Interface for Qdrant/ChromaDB vector database.

Stores:
  - Job description embeddings
  - Candidate profile embeddings
  - Skill embeddings

Provides:
  - Semantic search (find similar JDs, similar candidates)
  - Filtered search (by skills, location, experience range)
  - CRUD operations for vector collections
  - Batch insertion and retrieval
"""


class VectorStore:
    def __init__(self, collection_name: str, embedding_dim: int = 768):
        self.collection_name = collection_name
        self.embedding_dim = embedding_dim

    def create_collection(self):
        """Initialize collection with proper index configuration."""

    def insert(self, vector_id: str, embedding: list, payload: dict) -> bool:
        """Insert a single vector with metadata payload."""

    def insert_batch(self, vectors: list) -> int:
        """Insert multiple vectors. Returns count."""

    def search(self, query_embedding: list, filters: dict = None, top_k: int = 20) -> list:
        """Search for similar vectors with optional filters."""

    def get(self, vector_id: str) -> dict | None:
        """Retrieve a single vector by ID."""

    def delete(self, vector_id: str) -> bool:
        """Delete a vector by ID."""

    def update_payload(self, vector_id: str, payload: dict) -> bool:
        """Update metadata payload for existing vector."""
