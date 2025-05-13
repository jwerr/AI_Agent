# multi_agent/controller.py
from planner_agent import plan_steps
from executer_agent import execute_task
from verifier_agent import verify_result

query = input("🧠 Ask your AutoAgent: ")
plan = plan_steps(query)
print("🧭 Plan:", plan)

tasks = plan.split("\n")
for idx, task in enumerate(tasks, 1):
    if not task.strip(): continue
    print(f"\n🔧 Task {idx}: {task}")
    result = execute_task(task)
    print(f"✅ Result: {result}")
    feedback = verify_result(task, result)
    print(f"🔍 Verifier Feedback: {feedback}")
