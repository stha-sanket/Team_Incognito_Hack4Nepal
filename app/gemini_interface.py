import os
import json
import re
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

def extract_info_from_image(image_path):
    image = Image.open(image_path)

    prompt = '''
You are given an official scanned document image (e.g., citizenship, passport, or license).
Your task is to extract the information and return it in valid JSON format only, with no explanation, no markdown, no escape characters, and no code blocks like ```json or ```.
Structure your response using the following keys:
    {
        "country": "",
        "type": "",
        "citizenship_certificate_number": "",
        "full_name": "",
        "sex": "",
        "date_of_birth_ad": {
            "year": null,
            "month": "",
            "day": null
        },
        "birth_place": {
            "district": "",
            "municipality": "",
            "ward_no": null
        },
        "permanent_address": {
            "district": "",
            "municipality": "",
            "ward_no": null
        },
        "issuing_officer_name": "",
        "issuing_officer_title": "",
        "issuing_date_bs": ""
    }

Rules:
1. DO NOT wrap the output in quotes.
2. DO NOT use escape sequences (like \\n, \\t, etc.).
3. DO NOT return markdown formatting (like **, ```, or 'json').
4. If any field is missing or not visible, return null or an empty string "".
5. Output must be a valid JSON object, not a string representation of JSON.
6. Return the Document Type as "citizenship" if it is a citizenship document, "pan" if it is a PAN-card.

    Return only the raw JSON object. Nothing else.
    '''

    # Gemini request
    response = model.generate_content([prompt, image])
    text = response.text.strip()

    # Cleanup: remove ```json ... ```
    clean_text = re.sub(r"^```json|```$", "", text.strip(), flags=re.MULTILINE).strip()

    # Validate JSON
    try:
        return json.loads(clean_text)
    except json.JSONDecodeError:
        print("Invalid JSON from Gemini. Returning raw string.")
        return {"raw": clean_text}
