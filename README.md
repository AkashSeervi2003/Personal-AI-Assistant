# Personal AI Assistant (ScrapMate)

Your documents, chat-ready. Upload PDFs and ask questions; the assistant retrieves relevant chunks and responds with context-aware answers.

## Screenshots

Add your screenshots to the repository and update the paths below. Recommended folder: `docs/screenshots/` (already created). Drop your PNGs there and adjust paths.


- Login UI
  
<img width="1920" height="1080" alt="Screenshot (8)" src="https://github.com/user-attachments/assets/25d4af36-b379-4d5d-a5fb-b29d45923a6f" />



- Sign Up UI
  
<img width="1920" height="1080" alt="Screenshot (9)" src="https://github.com/user-attachments/assets/0243f8b8-3e4f-4eae-9754-bb55bb2a432e" />

- PDF upload UI
  
	![Upload PDFs](docs/screenshots/upload.png)

- Upload & Processing Status<img width="1781" height="750" alt="Screenshot 2025-11-10 045640" src="https://github.com/user-attachments/assets/1478a026-12db-42bb-8708-5b7d76b5f6ec" />

  
	![Upload & Processing](docs/screenshots/upload_processing.png)

- Conversation view (ask questions about your PDFs)
  
	![Chat view](docs/screenshots/chat.png)

- Conversation view (detailed answer with citations)
  
	![Conversation Detail](docs/screenshots/conversation.png)

> Tip: Drag images into the GitHub web UI or commit them locally under `docs/screenshots/` with names like `login.png`, `signup.png`, `upload.png`, `chat.png`.

## How it works

1. Upload PDFs in the sidebar.
2. The app extracts text, chunks it, and builds an embedding index.
	 - Primary: HuggingFace/FAISS when packages are available.
	 - Fallback: TF–IDF with cosine similarity (scikit‑learn) if transformers are missing.
3. Ask a question in the chat box.
4. A retriever finds the most relevant chunks for your query.
5. The LLM (Gemini via Google Generative AI) generates an answer grounded in those chunks.
6. Conversations are stored locally in a SQLite database for persistence.

## Quick start (Windows / PowerShell)

1. Python 3.10+ recommended. Create and activate a virtual environment:
	 - `python -m venv .venv`
	 - `& .\.venv\Scripts\Activate.ps1`

2. Install dependencies:
	 - `pip install -r requirements.txt`

3. Add your API key (required for Gemini):
	 - Create a `.env` file with a line: `GEMINI_API_KEY=your_key_here`

4. Run the app:
	 - `streamlit run app.py`

The app opens in your browser (default http://localhost:8501). You can change the port with `--server.port 8514`.

## Configuration

- Set your model and defaults in `src/config.py`.
- Environment variables: `.env` supports `GEMINI_API_KEY`.
- Local data:
	- SQLite file: `user_history.db` (ignored from Git by default).

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

## Troubleshooting

- “Missing API key” or model errors: add `GEMINI_API_KEY` in `.env`.
- Import errors for `sentence_transformers`/`langchain`: the app will fall back to TF‑IDF; for best results, install the full stack.
- Streamlit duplicate element ID: we use unique keys for buttons and inputs; if you add new widgets, give them unique `key` arguments.

## License

Add a license if you plan to share publicly (MIT is common). Create a `LICENSE` file at the repo root.

---


If you want, I can also generate the screenshots section for you once you upload images to `Images/` or provide links.





