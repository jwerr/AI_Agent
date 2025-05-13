import streamlit as st
from multi_agent.coordinator_agent import plan_and_execute
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# --- Page Setup ---
st.set_page_config(page_title="AutoAgent – RAG + LLM Assistant", layout="wide")
st.title("AutoAgent AI Assistant")

# --- Simulated User Profiles ---
user_list = ["User_1", "User_2", "Admin"]
st.sidebar.markdown("### 👤 Select User")
selected_user = st.sidebar.selectbox("User Profile", user_list)

# --- Persistent History Path ---
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

if "user_profiles" not in st.session_state:
    st.session_state.user_profiles = {}

if selected_user not in st.session_state.user_profiles:
    st.session_state.user_profiles[selected_user] = load_user_data()

user_data = st.session_state.user_profiles[selected_user]

# --- Project Description ---
st.markdown("""
### Project Description
AutoAgent is a powerful AI assistant that combines **Retrieval-Augmented Generation (RAG)** with **LLM-based reasoning** to automate document understanding, numeric analysis, and smart responses.

**Key Features:**
- Upload and analyze `.txt` documents
- Ask natural language questions
- Automatically uses RAG, score extraction, or rounding tools
- Stores full conversation history per user
- View and download past interactions
- See usage analytics and visual breakdowns
""")

# --- Upload Text Document (Multi-file Support) ---
st.markdown("### 📄 Upload Document(s) ")
uploaded_files = st.file_uploader("Upload one or more .txt files", type=["txt"], accept_multiple_files=True)

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
    st.success(f"✅ Uploaded {len(uploaded_files)} file(s) successfully!")

# --- Select File to Use ---
if user_data.get("uploaded_docs"):
    selected_doc = st.selectbox("📂 Select a document to use", user_data["uploaded_docs"])
    st.markdown(f"**Current document:** `{os.path.basename(selected_doc)}`")
else:
    selected_doc = None

# --- Input Section ---
st.markdown("### 💬 Ask a question or give a task")
user_input = st.text_input("What would you like the agent to do?", "")

if user_input.strip().lower() == "document":
    user_input = "Summarize the uploaded document"

# --- Submit ---
if st.button("Submit") and user_input:
    with st.spinner("🤖 Multi-agent reasoning..."):
        result = plan_and_execute(user_input)
        user_data["history"].append((user_input, result, "MultiAgent"))
        user_data["latest_answer"] = result
        save_user_data()

# --- Show Latest Answer ---
if user_data["latest_answer"]:
    st.markdown("### 🧾 Latest Answer")
    st.write(user_data["latest_answer"])

# --- Sidebar: User Profile & Conversation History ---
with st.sidebar:
    st.markdown(f"#### 👤 Active User: `{selected_user}`")

    st.markdown("### 🗂️ Conversation History")
    for i, (question, answer, tool) in enumerate(reversed(user_data["history"]), start=1):
        with st.expander(f"Q{i}: {question[:40]}..."):
            st.markdown(f"**Answer:** {answer}")
            st.markdown(f"🔧 **Tool Used:** `{tool}`")

    st.markdown("### 📥 Download History")
    history_data = json.dumps(user_data["history"], indent=2)
    st.download_button(
        label="📄 Download Conversation History",
        data=history_data,
        file_name=f"{selected_user.lower()}_autoagent_history.json",
        mime="application/json"
    )

    st.markdown("### ❌ Reset History")
    if st.button("Clear All History"):
        user_data["history"] = []
        user_data["chat_history"] = []
        user_data["latest_answer"] = ""
        user_data["uploaded_docs"] = []
        save_user_data()
        st.success("🧹 History cleared successfully!")

    st.markdown("---")
    st.markdown("### 📊 Usage Analytics")
    if user_data["history"]:
        df = pd.DataFrame(user_data["history"], columns=["Query", "Answer", "Tool"])
        tool_counts = Counter([item[2] for item in user_data["history"]])
        st.markdown("**Tool Usage**")
        st.bar_chart(pd.DataFrame.from_dict(tool_counts, orient='index', columns=["Usage"]))

        st.markdown("**Query Count**")
        st.write(f"Total queries submitted: {len(user_data['history'])}")
    else:
        st.markdown("No analytics yet. Ask a question to get started.")
