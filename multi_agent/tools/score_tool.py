import os
import re

def extract_and_average_from_doc(_: str = "") -> str:
    doc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../docs/example.txt"))

    if not os.path.exists(doc_path):
        return "❌ Document not found."

    with open(doc_path, "r", encoding="utf-8") as f:
        content = f.read()

    numbers = list(map(int, re.findall(r'\d+', content)))
    if not numbers:
        return "No scores found in the document."

    average = sum(numbers) / len(numbers)
    average_rounded = round(average, 2)
    count = len(numbers)

    return (
        f"📊 Extracted scores: {numbers}\n"
        f"🔢 Total scores: {count}\n"
        f"📈 Average score (rounded): {average_rounded}"
    )
