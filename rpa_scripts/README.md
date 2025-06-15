# Form Automation RPA Script

This RPA (Robotic Process Automation) script automates the process of filling out forms in the Document Application System.

## Prerequisites

1. Python 3.8 or higher
2. Chrome browser installed
3. The Django application running locally

## Installation

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the `rpa_scripts` directory with the following content:
```
USERNAME=your_username
PASSWORD=your_password
BASE_URL=http://localhost:8000
```

Replace `your_username` and `your_password` with your actual credentials.

## Usage

1. Make sure your Django application is running (usually on http://localhost:8000)

2. Run the automation script:
```bash
python form_automation.py
```

The script will:
- Log in to your account
- Fill out the citizenship application form
- Fill out the PAN card application form
- Fill out the contact form
- All with randomly generated data

## Features

- Automated form filling for all application types
- Random data generation using Faker
- Configurable through environment variables
- Error handling and logging
- Headless mode support (can run without opening browser window)

## Customization

- To run in headless mode, uncomment the line `chrome_options.add_argument("--headless")` in the script
- Modify the fake data generation in each form filling method to match your requirements
- Adjust the wait times (`time.sleep()`) if needed based on your system's performance

## Troubleshooting

1. If you get WebDriver errors:
   - Make sure Chrome is installed
   - Try updating the webdriver-manager: `pip install --upgrade webdriver-manager`

2. If form fields are not found:
   - Check if the field names match your Django form
   - Increase the wait time in WebDriverWait

3. If login fails:
   - Verify your credentials in the .env file
   - Check if the login URL is correct 