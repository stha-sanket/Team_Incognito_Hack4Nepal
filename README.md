gemini_doc_classifier/
│
├── 📁 docs/                      # Input documents (images, pdfs, txt)
│
├── 📁 app/                       # Core logic
│   ├── gemini_interface.py     # Handles Gemini API communication
│   ├── classifier.py           # Classifies documents based on Gemini output
│   ├── db.py                   # DB connection and insert/retrieve logic
│   └── utils.py                # (Optional) Helpers: file reading, cleaning
│
├── 📁 db/                        # Database-related files
│   └── schema.sql              # SQL schema to store classified documents
│
├── 📄 .env                       # API keys, DB credentials
├── 📄 main.py                    # Entry point: Load doc → classify → store in DB
├── 📄 requirements.txt           # Dependencies
└── 📄 README.md                  # How to run the project   