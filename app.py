import streamlit as st
from multi_agent.coordinator_agent import plan_and_execute
import os
import json
import pandas as pd
from collections import Counter

from dotenv import load_dotenv
load_dotenv()
# --- App Configuration ---
st.set_page_config(page_title="AutoAgent – RAG + LLM Assistant", layout="wide")
st.title("AutoAgent: Context-Aware AI Assistant")

# --- Simulated User Profiles ---
user_list = ["User", "User_2", "Admin"]
st.sidebar.header("👤 Select a User")
selected_user = st.sidebar.selectbox("Choose your profile", user_list)

# --- Define History File Path ---
history_dir = "user_histories"
os.makedirs(history_dir, exist_ok=True)
history_path = os.path.join(history_dir, f"{selected_user.lower()}_history.json")

# --- Load or Initialize User Data ---
def load_user_data():
    default_data = {
        "history": [],
        "chat_history": [],
        "latest_answer": "",
        "uploaded_docs": []
    }
    if os.path.exists(history_path):
        try:
            with open(history_path, "r") as f:
                data = json.load(f)
            for key in default_data:
                if key not in data:
                    data[key] = default_data[key]
            return data
        except Exception as e:
            st.warning(f"⚠️ Failed to load profile data: {e}")
    return default_data

def save_user_data():
    with open(history_path, "w") as f:
        json.dump(user_data, f, indent=2)

# --- Session State Handling ---
if "user_profiles" not in st.session_state:
    st.session_state.user_profiles = {}

if selected_user not in st.session_state.user_profiles:
    st.session_state.user_profiles[selected_user] = load_user_data()

user_data = st.session_state.user_profiles[selected_user]

# --- Project Overview ---
with st.expander("📘 About AutoAgent", expanded=True):
    st.markdown("""
    **AutoAgent** is a smart assistant that combines Retrieval-Augmented Generation (RAG) and large language model (LLM) reasoning to automate text document analysis and question answering.

    **Core Features:**
    - Upload and summarize `.txt` documents
    - Ask complex questions in natural language
    - Intelligent agent picks the right tools: RAG, scoring, rounding
    - Tracks personalized chat history
    - Download history and explore tool usage analytics
    """)

# --- Document Upload ---
st.markdown("### 📁 Upload Text Documents")
uploaded_files = st.file_uploader("Upload `.txt` files", type=["txt"], accept_multiple_files=True)
os.makedirs("docs", exist_ok=True)
if uploaded_files:
    for file in uploaded_files:
        safe_filename = f"{selected_user.lower()}_{file.name}"
        save_path = os.path.join("docs", safe_filename)
        with open(save_path, "wb") as f:
            f.write(file.getbuffer())
        if save_path not in user_data["uploaded_docs"]:
            user_data["uploaded_docs"].append(save_path)
    save_user_data()
    st.success(f"✅ Uploaded {len(uploaded_files)} file(s) successfully.")

# --- Document Selection ---
if user_data.get("uploaded_docs"):
    selected_doc = st.selectbox("📄 Choose a document to analyze", user_data["uploaded_docs"])
    st.caption(f"Using: `{os.path.basename(selected_doc)}`")
else:
    selected_doc = None

# --- Ask a Question ---
st.markdown("### Ask a Question or Give a Task")
user_input = st.text_input("e.g., Summarize the document, Extract key points, etc.")
if user_input.strip().lower() == "document":
    user_input = "Summarize the uploaded document"

# --- Submit & Execute ---
if st.button("Run") and user_input:
    with st.spinner("Running AI agents..."):
        result = plan_and_execute(user_input)
        user_data["history"].append((user_input, result, "MultiAgent"))
        user_data["latest_answer"] = result
        save_user_data()

# --- Display Answer ---
if user_data["latest_answer"]:
    st.markdown("### Latest Answer")
    st.success(user_data["latest_answer"])

# --- Sidebar: History, Analytics, Controls ---
with st.sidebar:
    st.subheader(f"User: {selected_user}")

    st.markdown("### 📚 History")
    for i, (query, answer, tool) in enumerate(reversed(user_data["history"]), 1):
        with st.expander(f"Q{i}: {query[:50]}"):
            st.markdown(f"**Answer:** {answer}")
            st.caption(f"🔧 Tool: `{tool}`")

    st.markdown("### ⬇️ Download History")
    st.download_button(
        "Download JSON",
        data=json.dumps(user_data["history"], indent=2),
        file_name=f"{selected_user}_history.json",
        mime="application/json"
    )

    st.markdown("### 🧹 Clear History")
    if st.button("Clear All"):
        user_data.update({
            "history": [],
            "chat_history": [],
            "latest_answer": "",
            "uploaded_docs": []
        })
        save_user_data()
        st.success("✅ History cleared.")

    st.markdown("---")
    st.markdown("### 📊 Tool Usage Stats")
    if user_data["history"]:
        df = pd.DataFrame(user_data["history"], columns=["Query", "Answer", "Tool"])
        tool_counts = Counter(df["Tool"])
        st.bar_chart(pd.DataFrame.from_dict(tool_counts, orient='index', columns=["Usage"]))
        st.caption(f"Total Queries: {len(user_data['history'])}")
    else:
        st.info("Submit a query to view analytics.")
