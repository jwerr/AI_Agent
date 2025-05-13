# AutoAgent – RAG + LLM Assistant

AutoAgent is an intelligent AI-powered assistant that blends Retrieval-Augmented Generation (RAG), multi-agent reasoning, and dynamic tool orchestration to respond to user queries about uploaded documents.

## Live Demo

Run locally:

```bash
streamlit run app.py
```

## Features

* Upload and query multiple `.txt` documents
* Multi-agent decision making using LangChain
* Dynamic tool usage: RAGSearch, ScoreAverager, SafeRounder
* Per-user simulated profiles with persistent history
* Conversation download and analytics
* Simple user interface using Streamlit

## Technology Stack

| Component    | Technology         |
| ------------ | ------------------ |
| Frontend     | Streamlit          |
| Backend      | Python + LangChain |
| LLM Provider | OpenAI API         |
| Embeddings   | FAISS + OpenAI     |
| Storage      | JSON-based history |

## File Structure

```
.
├── app.py                      # Main Streamlit app
├── config.yaml                 # Optional app config
├── docs/                       # Uploaded documents
├── user_histories/            # Per-user session logs
├── multi_agent/               # Coordinator, tools, agents
├── requirements.txt           # Dependencies
├── .env                        # API keys (not committed)
└── README.md
```

## Setup Instructions

1. **Clone the repository:**

```bash
git clone https://github.com/jwerr/autoagent.git
cd autoagent
```

2. **Create a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Add your OpenAI API key:**
   Create a `.env` file:

```
OPENAI_API_KEY=your-api-key-here
```

5. **Run the app:**

```bash
streamlit run app.py
```

## Example Use Cases

* Summarize uploaded content using retrieval-based QA
* Compute numeric scores from raw data text
* Ask general or contextual questions about documents
* Track tool usage and download history

## License

For academic and non-commercial use only.
