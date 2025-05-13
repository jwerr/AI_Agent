# multi_agent/planner_agent.py
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate

llm = OpenAI(temperature=0)

def plan_steps(query):
    query = query[:2000]  # Limit to 2000 characters
    prompt = PromptTemplate.from_template(
    "Break the following instruction into steps:\nInstruction: {query}\nSteps:"
    )
    return llm(prompt.format(query=query))
