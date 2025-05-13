import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Load documents from a folder
def load_all_docs(folder_path):
    docs = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith(".txt"):
            loader = TextLoader(file_path)
        elif filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        else:
            continue
        docs.extend(loader.load())
    return docs

# Load and split documents
raw_docs = load_all_docs("docs")
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = splitter.split_documents(raw_docs)

# Embed and build retriever
embedding = OpenAIEmbeddings(openai_api_key=openai_api_key)
vectorstore = FAISS.from_documents(docs, embedding)
retriever = vectorstore.as_retriever()

# LLM and QA chain
llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# Ask a question from your notes
while True:
    query = input("🔍 Ask something from your docs (or 'exit'): ")
    if query.lower() == "exit":
        break
    answer = qa_chain.run(query)
    print("💬 Answer:", answer)
