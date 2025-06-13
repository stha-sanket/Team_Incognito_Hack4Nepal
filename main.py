import os
from app.gemini_interface import extract_info_from_image
from app.classifier import classify_from_text
from app.file_storage import save_to_json

docs_path = "../gemini_doc_classifier/docs"
image_extensions = [".jpg", ".jpeg", ".png"]

for filename in os.listdir(docs_path):
    if any(filename.lower().endswith(ext) for ext in image_extensions):
        path = os.path.join(docs_path, filename)
        print(f"\n📷 Processing: {filename}")

        extracted = extract_info_from_image(path)
        print(f"🔍 Extracted:\n{extracted}")


        save_to_json(extracted, path)

print("\n🚀 Done processing all files.")
