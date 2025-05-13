from langchain.agents import Tool, initialize_agent
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_openai import OpenAI
from langchain.memory import ConversationBufferMemory
import streamlit as st
import os

# --- Custom Tools ---
from multi_agent.tools.rag_tool import rag_search
from multi_agent.tools.score_tool import extract_and_average_from_doc
from multi_agent.tools.rounding_tool import safe_round

# --- LLM & Tool Initialization ---
llm = OpenAI(temperature=0)
tools = load_tools(["llm-math", "wikipedia"], llm=llm)

# Add Custom Tools
tools.extend([
    Tool(name="RAGSearch", func=rag_search, description="Summarize or retrieve information from the uploaded document."),
    Tool(name="ScoreAverager", func=extract_and_average_from_doc, description="Extract numeric scores and compute their average."),
    Tool(name="SafeRounder", func=safe_round, description="Safely round numbers to desired precision.")
])

# --- Memory ---
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# --- Agent Configuration ---
agent_kwargs = {
    "prefix": (
        "You are an AI assistant with access to multiple tools.\n\n"
        "Use the RAGSearch tool when a question involves summarizing, answering from, or retrieving information from documents.\n"
        "Use the ScoreAverager tool only when asked to extract or calculate numeric scores.\n"
        "Use SafeRounder only to round numeric results.\n"
        "Never use 'Calculator' for functions like round(), len(), or string operations.\n"
        "Always end with: Final Answer: [your result here]."
        "You are a helpful AI assistant. Use prior interactions to answer more effectively.\n"
        "You have access to tools and a memory buffer.\n"
        "If the current question relates to an earlier one, reason over both."
    )
}

executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    memory=memory,
    verbose=True,
    agent_kwargs=agent_kwargs,
    handle_parsing_errors=True
)

# --- Task Execution Function ---
def execute_task(task: str, chat_memory: list = None):
    print("🧠 TASK:", task)

    # Add memory to agent from chat history
    if chat_memory:
        for item in chat_memory:
            executor.memory.chat_memory.add_user_message(item["content"]) if item["role"] == "human" \
                else executor.memory.chat_memory.add_ai_message(item["content"])

    result = executor.run(task)

    # Detect tool used (optional refinement)
    tool_used = "Unknown"
    if "score" in result.lower():
        tool_used = "ScoreAverager"
    elif "AutoAgent" in result or "document" in result:
        tool_used = "RAGSearch"
    elif "rounded" in result.lower():
        tool_used = "SafeRounder"

    # Save memory
    messages = executor.memory.chat_memory.messages
    chat_history = [{"role": m.type, "content": m.content} for m in messages]

    return result, tool_used, chat_history
