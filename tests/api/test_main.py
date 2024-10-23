import chromadb
import pytest
from chromadb.utils import embedding_functions
from httpx import ASGITransport, AsyncClient

from api.dependencies import get_chroma_client, get_cohere_embeddings
from api.main import app


def get_chroma_client_override():
    return chromadb.Client()


def get_cohere_embeddings_override():
    return embedding_functions.DefaultEmbeddingFunction()


app.dependency_overrides[get_chroma_client] = get_chroma_client_override
app.dependency_overrides[get_cohere_embeddings] = get_cohere_embeddings_override


@pytest.mark.anyio
async def test_add_document():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post(
            "/vector_store",
            json={
                "content": "Hoàng Sa và Trường Sa là của Việt Nam",
                "collection_name": "geography",
                "reference_id": "1",
            },
        )
        assert response.status_code == 200
        assert type(response.json()["ids"]) is list
