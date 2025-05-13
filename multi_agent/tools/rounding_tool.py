def safe_round(value: str) -> str:
    try:
        num = float(value)
        return f"✅ Rounded value: {round(num)}"
    except Exception as e:
        return f"❌ Could not round the input '{value}': {e}"
