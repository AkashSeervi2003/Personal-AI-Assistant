# Personal AI Assistant (ScrapMate)

Your documents, chat-ready. Upload PDFs and ask questions; the assistant retrieves relevant chunks and responds with context-aware answers.

## Screenshots


1. Login UI
  
<img width="1920" height="1080" alt="Screenshot (8)" src="https://github.com/user-attachments/assets/25d4af36-b379-4d5d-a5fb-b29d45923a6f" />



2. Sign Up UI
  
<img width="1920" height="1080" alt="Screenshot (9)" src="https://github.com/user-attachments/assets/0243f8b8-3e4f-4eae-9754-bb55bb2a432e" />

3. PDF upload UI
  
	<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/f1373f36-611d-4732-b6ff-0505ad088fdf" />


4. Upload & Processing Status

  <img width="1920" height="1080" alt="Screenshot (11)" src="https://github.com/user-attachments/assets/470e2dc4-2ed0-447f-9fb1-b8d930059c1c" />


5. Conversation view

  <img width="1920" height="1080" alt="Screenshot (12)" src="https://github.com/user-attachments/assets/7b72fec3-9321-46da-93b3-6de319a6894e" />



## How it works

1. Upload PDFs in the sidebar.
2. The app extracts text, chunks it, and builds an embedding index.
	 - Primary: HuggingFace/FAISS when packages are available.
	 - Fallback: TF–IDF with cosine similarity (scikit‑learn) if transformers are missing.
3. Ask a question in the chat box.
4. A retriever finds the most relevant chunks for your query.
5. The LLM (Gemini via Google Generative AI) generates an answer grounded in those chunks.
6. Conversations are stored locally in a SQLite database for persistence.



## Project structure

```
app.py                         # Streamlit app entry
requirements.txt               # Python dependencies
src/
	chat.py                      # Chat manager & LLM chain wiring
	embedding.py                 # Embedding manager (FAISS / TF‑IDF fallback)
	processor.py                 # PDF loading, text extraction, chunking
	history.py                   # SQLite for users, conversations, messages
	config.py                    # App configuration & model settings
	ui/theme.py                  # Global CSS and UI helpers
scripts/
	smoke_embed_test.py          # Minimal embedding sanity test
```










