from typing import List, Optional, Any
import numpy as np
from langchain_core.documents import Document
try:
    from langchain_core.retrievers import BaseRetriever
    from langchain_core.callbacks import CallbackManagerForRetrieverRun
    from langchain_core.pydantic_v1 import PrivateAttr
    _HAS_LC_CORE = True
except Exception:
    _HAS_LC_CORE = False
from src.config import Config

# Check for sentence-transformers explicitly (some wrappers import without it installed)
try:
    from sentence_transformers import SentenceTransformer  # noqa: F401
    _HAS_SENTENCE_TRANSFORMERS = True
except Exception:
    _HAS_SENTENCE_TRANSFORMERS = False

# Try primary embedding backend; fall back to TF-IDF if unavailable
try:
    from langchain_community.embeddings import HuggingFaceEmbeddings  # type: ignore
    from langchain_community.vectorstores import FAISS  # type: ignore
    _HAS_LC_HF = True
except Exception:
    _HAS_LC_HF = False

# Final gate: only use HuggingFaceEmbeddings when both are available
_HAS_ST = _HAS_LC_HF and _HAS_SENTENCE_TRANSFORMERS

if not _HAS_ST:
    from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore
    from sklearn.metrics.pairwise import cosine_similarity  # type: ignore

class EmbeddingManager:
    """
    Manages embeddings and retrieval using LangChain components.
    Uses SentenceTransformerEmbeddings for embeddings and FAISS for vector storage.
    """
    def __init__(self):
        # Initialize the embedding model using LangChain's HuggingFaceEmbeddings when available
        self.vectorstore = None
        self.retriever = None
        if _HAS_ST:
            self.embedding_model = HuggingFaceEmbeddings(
                model_name=Config.EMBEDDING_MODEL
            )
        else:
            # TF-IDF fallback components
            self.embedding_model = None
            self._tfidf: Optional[TfidfVectorizer] = None
            self._tfidf_matrix = None
            self._docs: List[Document] = []

    def create_embeddings(self, documents: List[Document]):
        """
        Creates embeddings for documents and stores them in FAISS.
        
        Args:
            documents: List of LangChain Document objects
        """
        try:
            if _HAS_ST:
                # Create FAISS index from documents using LangChain
                self.vectorstore = FAISS.from_documents(
                    documents,
                    self.embedding_model,
                )
                # Create a retriever from the vector store
                self.retriever = self.vectorstore.as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": Config.TOP_K},
                )
            else:
                # Build TF-IDF matrix as a lightweight fallback
                self._docs = documents
                texts = [d.page_content for d in documents]
                self._tfidf = TfidfVectorizer(max_features=4096, ngram_range=(1, 2))
                self._tfidf_matrix = self._tfidf.fit_transform(texts)

                if _HAS_LC_CORE:
                    class TfidfRetriever(BaseRetriever):  # type: ignore
                        """Pydantic-compatible retriever using PrivateAttr storage."""
                        _tfidf: Any = PrivateAttr()
                        _matrix: Any = PrivateAttr()
                        _docs: List[Document] = PrivateAttr(default=[])

                        def __init__(self, tfidf, matrix, docs):
                            super().__init__()
                            self._tfidf = tfidf
                            self._matrix = matrix
                            self._docs = docs

                        def _get_relevant_documents(
                            self,
                            query: str,
                            *,
                            run_manager: CallbackManagerForRetrieverRun,
                        ) -> List[Document]:  # noqa: D401
                            q_vec = self._tfidf.transform([query])
                            sims = cosine_similarity(q_vec, self._matrix)[0]
                            idxs = np.argsort(-sims)[: Config.TOP_K]
                            return [self._docs[i] for i in idxs]

                        async def _aget_relevant_documents(
                            self,
                            query: str,
                            *,
                            run_manager: CallbackManagerForRetrieverRun,
                        ) -> List[Document]:
                            return self._get_relevant_documents(query, run_manager=run_manager)

                    self.retriever = TfidfRetriever(self._tfidf, self._tfidf_matrix, self._docs)
                else:
                    # Minimal fallback retriever (not compatible with RetrievalQA chain)
                    class SimpleTfidfRetriever:
                        def __init__(self, tfidf, matrix, docs):
                            self._tfidf = tfidf
                            self._matrix = matrix
                            self._docs = docs

                        def get_relevant_documents(self, query: str) -> List[Document]:
                            q_vec = self._tfidf.transform([query])
                            sims = cosine_similarity(q_vec, self._matrix)[0]
                            idxs = np.argsort(-sims)[: Config.TOP_K]
                            return [self._docs[i] for i in idxs]

                    self.retriever = SimpleTfidfRetriever(self._tfidf, self._tfidf_matrix, self._docs)
            return True
        except Exception as e:
            print(f"Error creating embeddings: {str(e)}")
            return False

    def search(self, query: str, k: Optional[int] = None) -> List[Document]:
        """
        Searches for relevant documents based on the query.
        
        Args:
            query: The search query
            k: Number of documents to retrieve (defaults to Config.TOP_K)
            
        Returns:
            List[Document]: A list of relevant Document objects
        """
        if not k:
            k = Config.TOP_K
            
        if (not _HAS_ST and not self._tfidf) or ( _HAS_ST and not self.vectorstore) or not self.retriever:
            return []
            
        try:
            # Use the retriever to get relevant documents
            relevant_docs = self.retriever.get_relevant_documents(query)
            return relevant_docs
        except Exception as e:
            print(f"Error during search: {str(e)}")
            return []