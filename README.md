# DocuMind 🧠📄

DocuMind is a multimodal Retrieval-Augmented Generation (RAG) assistant that lets you upload documents in multiple formats and chat with their content. It combines Google's Gemini models with a local FAISS vector store for fast, accurate, source-grounded answers.

## Features

- 📂 **Multi-format ingestion** — PDF, Word (.docx), plain text, CSV, Excel, email (.eml/.msg), and web pages
- 🔍 **Semantic search** — HuggingFace sentence embeddings + FAISS vector index
- 🤖 **LLM-powered answers** — Google Gemini (`gemini-2.5-flash`) via LangChain
- 💬 **Conversational interface** — built with Streamlit
- ⚡ **Fast local retrieval** — no external vector DB required

## Tech Stack

| Component | Tool |
|---|---|
| LLM | Google Gemini API (`google-generativeai`, `langchain-google-genai`) |
| Orchestration | LangChain |
| Embeddings | HuggingFace (`langchain-huggingface`) |
| Vector Store | FAISS |
| Document Loaders | `PyPDFLoader`, `WebBaseLoader`, `TextLoader`, `Docx2txtLoader`, `CSVLoader`, `UnstructuredExcelLoader`, `UnstructuredEmailLoader` |
| Frontend | Streamlit |

## Project Structure

```
documind/
├── app.py                 # Streamlit entry point
├── rag_pipeline.py         # Document loading, chunking, embedding, retrieval, and QA chain
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/documind.git
cd documind
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

### 4. Add your API key
Create a `.env` file in the project root:
```
GOOGLE_API_KEY=your_gemini_api_key_here
```
Get a free key at [Google AI Studio](https://aistudio.google.com/app/apikey).

### 5. Run locally
```bash
streamlit run app.py
```

## Usage

1. Launch the app.
2. Upload one or more documents (PDF, DOCX, CSV, XLSX, TXT, or EML).
3. Wait for DocuMind to process and index the content.
4. Ask questions in the chat box — answers are generated from your documents.

## Environment Variables

| Variable | Description |
|---|---|
| `GOOGLE_API_KEY` | Your Gemini API key from Google AI Studio |

## Known Limitations

- Free-tier Gemini API keys have rate limits (requests/minute and per-day quotas).
- Large documents may take longer to embed on first upload.

## Roadmap

- [ ] Add image/multimodal document support (charts, scanned pages)
- [ ] Persistent vector store across sessions
- [ ] Source citation highlighting in the UI

## License

MIT
