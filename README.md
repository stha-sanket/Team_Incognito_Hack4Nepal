# Team Incognito Hack4Nepal Project

This is a Django-based web application for the Hack4Nepal hackathon.

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- On Windows:
```bash
venv\Scripts\activate
```
- On macOS/Linux:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

The server will start at http://127.0.0.1:8000/

# Gemini Doc Classifier 📄🔍

![Document Classification](https://via.placeholder.com/800x400?text=Gemini+Doc+Classifier)  <!-- Replace with actual banner -->

An AI-powered document classification and information extraction system using Google Gemini Pro Vision API. Process scanned documents and get structured JSON output with just a few lines of code.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub stars](https://img.shields.io/github/stars/your-username/gemini-doc-classifier?style=social)](https://github.com/your-username/gemini-doc-classifier)

## Features ✨

- Automatic document type classification (Citizenship, Passport, License etc.)
- 📑 Key field extraction: names, dates, addresses, ID numbers
- 🚀 Lightning-fast processing via Gemini Pro Vision API
- 🗃️ Clean JSON output without markdown artifacts
- 📁 Batch processing of multiple documents
- 🔧 Modular design for easy customization

## Quick Start 🚀

### Prerequisites
- Python 3.8+
- Google Gemini API key
- Scanned documents (JPG, PNG)

### Installation
```bash
git clone https://github.com/your-username/gemini_doc_classifier.git
cd gemini_doc_classifier
pip install -r requirements.txt