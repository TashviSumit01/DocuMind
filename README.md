# DocuMind 🧠📄

DocuMind is a multimodal Retrieval-Augmented Generation (RAG) assistant that lets you upload documents in multiple formats and chat with their content. It combines Groq's fast LLM inference with Google's Gemini for image understanding, backed by a local FAISS vector store for accurate, source-grounded answers.

## Features
- 📂 **Multi-format ingestion** — PDF, Word (.docx), plain text, CSV, Excel, email (.eml/.msg), and web pages
- 🔍 **Semantic search** — HuggingFace sentence embeddings + FAISS vector index
- 🤖 **LLM-powered answers** — Groq (`llama-3.3-70b-versatile`) via LangChain for text queries, Google Gemini (`gemini-2.5-flash`) for image/multimodal processing
- 💬 **Conversational interface** — built with Streamlit, with persistent chat history
- ⚡ **Fast local retrieval** — no external vector DB required

## Tech Stack
| Component | Tool |
|---|---|
| Primary LLM | Groq (`llama-3.3-70b-versatile`) via `langchain-groq` |
| Image Processing | Google Gemini (`gemini-2.5-flash`) via `langchain-google-genai` |
| Orchestration | LangChain |
| Embeddings | HuggingFace (`langchain-huggingface`) |
| Vector Store | FAISS |
| Document Loaders | PyPDFLoader, WebBaseLoader, TextLoader, Docx2txtLoader, CSVLoader, UnstructuredExcelLoader, UnstructuredEmailLoader |
| Frontend | Streamlit |

## Project Structure

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/TashviSumit01/DocuMind.git
cd DocuMind
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your API keys
Create a `.env` file in the project root:

Get a free Groq key at [console.groq.com](https://console.groq.com) and a Gemini key at [Google AI Studio](https://aistudio.google.com).

### 5. Run locally
```bash
streamlit run app.py
```

## Usage
1. Launch the app.
2. Upload one or more documents (PDF, DOCX, CSV, XLSX, TXT, or EML).
3. Wait for DocuMind to process and index the content.
4. Ask questions in the chat box — text queries are answered by Groq, image-based queries are handled by Gemini.

## Environment Variables
| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key |
| `GOOGLE_API_KEY` | Your Gemini API key from Google AI Studio |

## Known Limitations
- Free-tier Gemini API keys have rate limits (requests/minute and per-day quotas).
- Large documents may take longer to embed on first upload.

## Roadmap
- [ ] Persistent vector store across sessions
- [ ] Source citation highlighting in the UI
- [ ] Live demo link

## License
MIT
