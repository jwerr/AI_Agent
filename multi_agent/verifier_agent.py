# multi_agent/verifier_agent.py

from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate

llm = OpenAI(temperature=0)

def verify_result(task, result):
    # Custom tool usage guard
    if any(keyword in result.lower() for keyword in ["rounded", "decimal", "📈 average", "already", "final score"]):
        return (
            "✅ Verification: The result already includes a rounded score.\n"
            "ℹ️ No need to call the Calculator tool again. Value appears final."
        )

    # Otherwise, let the LLM judge accuracy
    prompt = PromptTemplate.from_template(
        "You are an AI verifier. Check if the result for the task is correct:\n\n"
        "Task: {task}\n\nResult: {result}\n\n"
        "Is the result correct and complete? Answer briefly."
    )
    return llm(prompt.format(task=task, result=result))
