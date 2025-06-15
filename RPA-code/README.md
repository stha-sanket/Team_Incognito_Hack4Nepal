# Team_Incognito_Hack4Nepal
This is our automation project made during hack for nepal, NCIT college

# RPA Automation Scripts

This directory contains RPA (Robotic Process Automation) scripts for automating various tasks.

## Directory Structure

```
RPA-code/
├── website_automation/    # Scripts for website data entry automation
└── google_forms/         # Scripts for Google Forms automation
```

## Website Automation

The website automation script automates data entry tasks on a simulated website. Features include:
- Form field detection and filling
- Data validation
- Error handling
- Progress tracking

## Google Forms Automation

The Google Forms automation script handles automated form submissions. Features include:
- Automated form field population
- File upload handling
- Response verification
- Batch processing capabilities

## Setup and Usage

1. Install dependencies:
```bash
pip install selenium
pip install webdriver_manager
pip install pandas
```

2. Configure webdriver:
```python
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
```

3. Run the scripts:
```bash
# For website automation
python website_automation/main.py

# For Google Forms automation
python google_forms/main.py
```
