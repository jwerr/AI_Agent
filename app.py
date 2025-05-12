from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import initialize_agent
from langchain_openai import OpenAI  # NEW: use this instead of old deprecated one
import os
from dotenv import load_dotenv

load_dotenv()  # Loads from .env file

llm = OpenAI(temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))  # Pass key securely

tools = load_tools(["llm-math"], llm=llm)

agent = initialize_agent(
    tools, llm, agent="zero-shot-react-description", verbose=True
)

print(agent.run("What is the square root of 425 divided by 5?"))
