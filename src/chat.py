from typing import List
import time
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:  # Fallback if package structure changes
    ChatGoogleGenerativeAI = None

from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain.schema import Document
from langchain.prompts import PromptTemplate
from langchain.schema.messages import SystemMessage, HumanMessage
from src.config import Config
import google.generativeai as genai


class ChatManager:
    """
    Manages chat interactions using LangChain components.
    Uses LangChain's RetrievalQA for handling conversational RAG.
    """
    def __init__(self, api_key: str):
        """
        Initialize the ChatManager with the specified API key.

        Args:
            api_key: The API key for the LLM service
        """
        self.api_key = api_key
        self.memory = None
        self.chain = None
        self.llm = None
        self._initialize_components()

    def _initialize_components(self):
        """
        Initialize LangChain components for the chat system.
        Sets up the LLM, memory, and creates the conversation chain.
        """
        # Initialize conversation memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="result"
        )

        # Initialize the LLM with retry logic
        try:
            if ChatGoogleGenerativeAI:
                self.llm = ChatGoogleGenerativeAI(
                    model=Config.MODEL_NAME,
                    google_api_key=self.api_key,
                    temperature=Config.LLM_TEMPERATURE,
                    max_output_tokens=Config.MAX_TOKENS,
                )
            else:
                # Fallback: raw Generative AI client wrapper
                genai.configure(api_key=self.api_key)
                self.llm = None  # We'll handle direct calls manually
        except Exception as e:
            print(f"Primary LLM init failed: {e}. Falling back to gemini-2.0-flash")
            try:
                if ChatGoogleGenerativeAI:
                    self.llm = ChatGoogleGenerativeAI(
                        model="gemini-2.0-flash",
                        google_api_key=self.api_key
                    )
                else:
                    genai.configure(api_key=self.api_key)
                    self.llm = None
            except Exception as e2:
                print(f"Fallback LLM init failed: {e2}")
                self.llm = None

    def _create_chain(self, retriever):
        """
        Creates a retrieval QA chain with the specified retriever.

        Args:
            retriever: The document retriever to use

        Returns:
            The created conversation chain
        """
        # System prompt template
        system_template = """You are a helpful assistant that answers questions based on the provided context.
        If you cannot find the answer in the context, acknowledge that and provide general information if possible.
        Always cite your sources when the information comes from the provided context.

        Context:
        {context}

        Question: {question}
        """

        # Create prompt templates
        qa_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=system_template
        )

        # Create the chain. Some LangChain versions require dict for chain_type_kwargs and
        # may validate retriever type strictly. We standardize input for compatibility.
        self.chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            memory=self.memory,
            return_source_documents=True,
            chain_type_kwargs={"prompt": qa_prompt},
            verbose=False,
        )

        return self.chain

    def generate_response(self, query: str, context_docs: List[Document]) -> str:
        """
        Generate a response based on the query and retrieved context documents.

        Args:
            query: The user's question
            context_docs: List of context documents retrieved for the query

        Returns:
            str: The generated response
        """
        # Extract text from documents
        context_texts = [doc.page_content for doc in context_docs]
        context_text = "\n".join(context_texts)

        if not self.chain:
            # Handle direct LLM call if chain isn't set up
            try:
                if self.llm:
                    messages = [
                        SystemMessage(content=f"You are a helpful assistant that answers questions based on the provided context. If you cannot find the answer in the context, say so.\n\nContext:\n{context_text}"),
                        HumanMessage(content=query)
                    ]
                    response = self.llm(messages)
                    return response.content
                else:
                    # Raw fallback using google-generativeai
                    model_name = Config.MODEL_NAME or "gemini-2.0-flash"
                    model = genai.GenerativeModel(model_name)
                    prompt = (
                        "You are a helpful assistant that answers questions based on the provided context. "
                        "If you cannot find the answer in the context, say so.\n\nContext:\n" + context_text + "\n\nQuestion: " + query
                    )
                    result = model.generate_content(prompt)
                    return getattr(result, "text", "(No response)")

            except Exception as e:
                print(f"Error generating response: {str(e)}")
                # Implement retry logic
                for attempt in range(3):
                    try:
                        time.sleep(1)  # Wait before retry
                        if self.llm:
                            response = self.llm(messages)
                            return response.content
                        else:
                            model = genai.GenerativeModel(Config.MODEL_NAME or "gemini-2.0-flash")
                            result = model.generate_content(prompt)
                            return getattr(result, "text", "(No response)")
                    except Exception as retry_e:
                        print(f"Retry {attempt+1} failed: {str(retry_e)}")

                return "I encountered an error while processing your request. Please try again later."
        else:
            # Use the chain if available
            try:
                result = self.chain.invoke({"query": query})
                return result.get("result", "(No result key)")
            except Exception as e:
                print(f"Chain error: {str(e)}")
                # Fall back to direct LLM call
                return self.generate_response(query, context_docs)

    def set_retriever(self, retriever):
        """
        Set the retriever and create a conversation chain.

        Args:
            retriever: The document retriever to use
        """
        # Only build RetrievalQA chain if we have a LangChain LLM instance
        # and a retriever compatible with RetrievalQA (BaseRetriever).
        try:
            from langchain_core.retrievers import BaseRetriever  # type: ignore
            is_valid = isinstance(retriever, BaseRetriever) and self.llm is not None
        except Exception:
            is_valid = self.llm is not None and hasattr(retriever, "get_relevant_documents")

        if is_valid:
            self._create_chain(retriever)
        else:
            # Fallback: rely on direct generate_response passing context docs.
            self.chain = None

    def reset_conversation(self):
        """
        Reset the conversation history.
        """
        if self.memory:
            self.memory.clear()

    def get_conversation_history(self):
        """
        Get the current conversation history.

        Returns:
            The conversation history
        """
        if self.memory:
            return self.memory.chat_memory.messages
        return []
