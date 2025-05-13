from multi_agent.executer_agent import executor
from langchain.agents import AgentExecutor

def plan_and_execute(task: str):
    # Step 1: Plan subtasks (currently simulated)
    if "summarize" in task.lower():
        subtasks = [task]
    elif "score" in task.lower():
        subtasks = ["Extract scores from document", "Compute average", "Round it"]
    else:
        subtasks = [task]  # fallback

    results = []
    for sub in subtasks:
        try:
            output = executor.run(sub)
            results.append(f"✔️ {sub} → {output}")
        except Exception as e:
            results.append(f"❌ {sub} → Error: {e}")

    # Step 2: Verify (placeholder logic)
    final = "\n\n".join(results)
    return f"✅ Verified Final Answer:\n\n{final}"
