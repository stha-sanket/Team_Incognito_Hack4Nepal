import os
import json
from datetime import datetime

OUTPUT_DIR = "../gemini_doc_classifier/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_to_json(content, image_path):
    data = {
        "contents": content,
        "image_path": image_path,
        "created_at": datetime.now().isoformat(),
    }
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    json_file = os.path.join(OUTPUT_DIR, f"{base_name}.json")

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"✅ JSON saved: {json_file}")
