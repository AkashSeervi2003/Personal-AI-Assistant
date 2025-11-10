from src.embedding import EmbeddingManager
from langchain_core.documents import Document

if __name__ == "__main__":
    em = EmbeddingManager()
    docs = [
        Document(page_content="The quick brown fox jumps over the lazy dog."),
        Document(page_content="Streamlit makes it easy to build ML apps."),
        Document(page_content="Retrieval augmented generation improves accuracy by grounding answers in documents."),
    ]
    ok = em.create_embeddings(docs)
    print("embeddings_created:", ok)
    res = em.search("What improves accuracy?", k=2)
    print("top_docs:", [d.page_content[:80] for d in res])
