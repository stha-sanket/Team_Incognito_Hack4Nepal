def classify_from_text(response_text):
    text = response_text
    if "citizenship" in text:
        return "Citizenship"
    elif "pan" in text:
        return "pan"
    else:
        return "Others"
