from typing import Optional, List, Dict, Any
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from app.config import settings
import uuid

openai_client = OpenAI(api_key=settings.openai_api_key)

qdrant_client: Optional[QdrantClient] = None
COLLECTION_NAME = settings.qdrant_collection_name
EMBEDDING_DIMENSION = 1536


def init_qdrant() -> QdrantClient:
    """Initialize Qdrant client and create collection if needed."""
    global qdrant_client
    qdrant_client = QdrantClient(url=settings.qdrant_url)

    try:
        qdrant_client.get_collection(COLLECTION_NAME)
    except Exception:
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=EMBEDDING_DIMENSION, distance=Distance.COSINE),
        )

    return qdrant_client


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk)

        start = end - overlap if end < len(text) else len(text)

    return chunks if chunks else [""]


def create_embedding(text: str) -> List[float]:
    """Create embedding using OpenAI API."""
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    return response.data[0].embedding


def create_embeddings_batch(texts: List[str]) -> List[List[float]]:
    """Batch create embeddings for multiple texts."""
    embeddings = []
    for text in texts:
        embedding = create_embedding(text)
        embeddings.append(embedding)

    return embeddings


def store_chunks_in_qdrant(document_id: int, chunks: List[str], embeddings: List[List[float]]) -> List[str]:
    """Store document chunks and their embeddings in Qdrant."""
    global qdrant_client
    if not qdrant_client:
        qdrant_client = init_qdrant()

    # Ensure collection exists
    try:
        qdrant_client.get_collection(COLLECTION_NAME)
    except Exception:
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=EMBEDDING_DIMENSION, distance=Distance.COSINE),
        )

    vector_ids = []

    for chunk_idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        vector_id = str(uuid.uuid4())
        vector_ids.append(vector_id)

        point = PointStruct(
            id=hash(vector_id) % (2**31),
            vector=embedding,
            payload={
                "document_id": document_id,
                "chunk_index": chunk_idx,
                "text": chunk,
            },
        )

        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=[point],
        )

    return vector_ids


def search_similar(query: str, top_k: int = 5, document_id: Optional[int] = None) -> List[Dict[str, Any]]:
    """Search Qdrant for similar content."""
    global qdrant_client
    if not qdrant_client:
        init_qdrant()

    query_embedding = create_embedding(query)

    filter_condition = None
    if document_id:
        filter_condition = Filter(
            must=[
                FieldCondition(key="document_id", match=MatchValue(value=document_id))
            ]
        )

    results = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        query_filter=filter_condition,
        limit=top_k,
    ).points

    return [
        {
            "document_id": result.payload["document_id"],
            "chunk_index": result.payload["chunk_index"],
            "text": result.payload["text"],
            "score": result.score,
        }
        for result in results
    ]
