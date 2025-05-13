from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAI, OpenAIEmbeddings
from pathlib import Path
import os
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain


def rag_search(query: str) -> str:
    if query.strip().lower() in {"document", "file", "this", "text"}:
        query = "Summarize the uploaded document"
    print(" RAG Query:", query)

    doc_path = Path(__file__).parent.parent.parent / "docs" / "example.txt"
    if not doc_path.exists():
        return f" Document not found at: {doc_path}"

    try:
        loader = TextLoader(str(doc_path), encoding="utf-8")
        raw_docs = loader.load()
        print(f"📄 Loaded {len(raw_docs)} documents")
    except Exception as e:
        return f"❌ Failed to load document at {doc_path}\nError: {e}"

    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = splitter.split_documents(raw_docs)
    if len(docs) > 20:
        docs = docs[:20]
    print(f"📚 Using {len(docs)} chunks for FAISS")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "❌ OPENAI_API_KEY is missing. Check .env file."

    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    vectorstore = FAISS.from_documents(docs, embeddings)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    llm = OpenAI(temperature=0)

    
    prompt_template = PromptTemplate.from_template("""
    You are a helpful assistant. Use the following context from a document to answer the question.
    If the answer is not explicitly stated, infer from context. Avoid saying "I don't know".

    Context:
    {context}

    Question:
    {question}

    Answer:
    """)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt_template},
        return_source_documents=True
    )


    try:
        result = qa_chain(query)
        answer = result.get("result", "⚠️ No answer returned.")
        sources = result.get("source_documents", [])
        print(f"🧠 Top retrieved docs:\n{[doc.page_content[:100] for doc in sources]}")
    except Exception as e:
        return f"❌ RAG failed.\nError: {e}"

    if not sources:
        return "⚠️ No relevant content found for your query."

    return f"{answer.strip()}"

