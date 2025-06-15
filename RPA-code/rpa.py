import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# --- Configuration ---
WEBSITE_URL = "http://127.0.0.1:8000/"
USERNAME = "admin"
PASSWORD = "123"
DATA_FILE = "data.json"

# --- Common Locators ---
LOGIN_PAGE_LINK_XPATH = "/html/body/div[2]/div/div[1]/div/a[2]"
USERNAME_FIELD_ID = "id_username"
PASSWORD_FIELD_ID = "id_password"
LOGIN_BUTTON_XPATH = "/html/body/div[2]/div/div/div/div/div[2]/form/div[3]/button"

# --- Page-Specific Locators ---
# Citizenship
CITIZENSHIP_PAGE_LINK_XPATH = "//*[@id='navbarNav']/ul[1]/li[2]/a"
CITIZENSHIP_NEXT_BTN_XPATH = "//*[@id='citizenshipForm']/div[3]/button[2]"
CITIZENSHIP_SUBMIT_BTN_XPATH = "//*[@id='citizenshipForm']/div[3]/button[3]"

# Pan Card
PAN_PAGE_LINK_XPATH = "//*[@id='navbarNav']/ul[1]/li[3]/a"
PAN_NEXT_BTN_XPATH = "//*[@id='panForm']/div[3]/button[2]"
PAN_SUBMIT_BTN_XPATH = "//*[@id='panForm']/div[3]/button[3]"

# Common Form Field IDs (assuming they are the same on both pages)
FULL_NAME_FIELD_ID = "full_name"
SEX_DROPDOWN_ID = "sex"
BIRTH_YEAR_FIELD_ID = "birth_year"
BIRTH_MONTH_DROPDOWN_ID = "birth_month"
BIRTH_DAY_FIELD_ID = "birth_day"


def load_data(file_path):
    """Loads records from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Data file not found at {file_path}")
        return []

def fill_common_details(driver, record):
    """Fills the form fields that are common to both forms."""
    # 1. Enter Full Name
    driver.find_element(By.ID, FULL_NAME_FIELD_ID).send_keys(record['full_name'])
    print(f"  - Entered name: {record['full_name']}")

    # 2. Select Sex
    sex_dropdown = Select(driver.find_element(By.ID, SEX_DROPDOWN_ID))
    sex_value = record['sex'].lower()
    if sex_value == 'male':
        sex_dropdown.select_by_visible_text('Male')
        print("  - Selected sex: Male")
    elif sex_value == 'female':
        sex_dropdown.select_by_visible_text('Female')
        print("  - Selected sex: Female")
    else:
        sex_dropdown.select_by_visible_text('Other')
        print("  - Selected sex: Other")

    # 3. Enter Birthdate
    driver.find_element(By.ID, BIRTH_YEAR_FIELD_ID).send_keys(record['birth_year'])
    month_dropdown = Select(driver.find_element(By.ID, BIRTH_MONTH_DROPDOWN_ID))
    month_dropdown.select_by_visible_text(record['birth_month'])
    driver.find_element(By.ID, BIRTH_DAY_FIELD_ID).send_keys(record['birth_day'])
    print(f"  - Entered birthdate: {record['birth_day']}/{record['birth_month']}/{record['birth_year']}")


def process_citizenship_form(driver, wait, record):
    """Navigates to and completes the citizenship form."""
    print(f"\n--- Processing CITIZENSHIP for: {record['full_name']} ---")
    try:
        # Navigate to the Citizenship page
        wait.until(EC.element_to_be_clickable((By.XPATH, CITIZENSHIP_PAGE_LINK_XPATH))).click()
        
        # Wait for a key element to ensure the page has loaded
        wait.until(EC.presence_of_element_located((By.ID, FULL_NAME_FIELD_ID)))
        
        # Fill in the details
        fill_common_details(driver, record)
        
        # Click Next and Submit
        driver.find_element(By.XPATH, CITIZENSHIP_NEXT_BTN_XPATH).click()
        time.sleep(0.5) # Small pause
        driver.find_element(By.XPATH, CITIZENSHIP_SUBMIT_BTN_XPATH).click()
        print(f"  - Citizenship form submitted successfully!")

    except (TimeoutException, NoSuchElementException) as e:
        print(f"An error occurred while processing citizenship for {record['full_name']}: {e}")

def process_pan_form(driver, wait, record):
    """Navigates to and completes the PAN card form."""
    print(f"\n--- Processing PAN CARD for: {record['full_name']} ---")
    try:
        # Navigate to the Pan Card page
        wait.until(EC.element_to_be_clickable((By.XPATH, PAN_PAGE_LINK_XPATH))).click()

        # Wait for a key element to ensure the page has loaded
        wait.until(EC.presence_of_element_located((By.ID, FULL_NAME_FIELD_ID)))

        # Fill in the details
        fill_common_details(driver, record)

        # Click Next and Submit
        driver.find_element(By.XPATH, PAN_NEXT_BTN_XPATH).click()
        time.sleep(0.5) # Small pause
        driver.find_element(By.XPATH, PAN_SUBMIT_BTN_XPATH).click()
        print(f"  - Pan Card form submitted successfully!")
        
    except (TimeoutException, NoSuchElementException) as e:
        print(f"An error occurred while processing Pan Card for {record['full_name']}: {e}")


def main():
    """Main function to run the RPA bot."""
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        # --- 1. Login Process (Happens only once) ---
        print("Navigating to the website...")
        driver.get(WEBSITE_URL)

        print("Logging in...")
        wait.until(EC.element_to_be_clickable((By.XPATH, LOGIN_PAGE_LINK_XPATH))).click()
        wait.until(EC.presence_of_element_located((By.ID, USERNAME_FIELD_ID))).send_keys(USERNAME)
        driver.find_element(By.ID, PASSWORD_FIELD_ID).send_keys(PASSWORD)
        driver.find_element(By.XPATH, LOGIN_BUTTON_XPATH).click()
        
        wait.until(EC.presence_of_element_located((By.XPATH, CITIZENSHIP_PAGE_LINK_XPATH)))
        print("Login successful.")

        # --- 2. Process Data Records ---
        records = load_data(DATA_FILE)
        if not records:
            print("No data to process. Exiting.")
            return

        for record in records:
            # Use .get() to safely access 'type' and default to "" if not found
            # Use .lower() to make the check case-insensitive (e.g., "Pan" and "pan" both work)
            record_type = record.get("type", "").lower()

            if record_type == "citizenship":
                process_citizenship_form(driver, wait, record)
            elif record_type == "pan":
                process_pan_form(driver, wait, record)
            else:
                print(f"\n--- SKIPPING record for '{record.get('full_name', 'N/A')}' ---")
                print(f"  - Reason: Unknown or unsupported type '{record.get('type', 'None')}'")

            time.sleep(1) # Pause between processing records

        print("\n--- All applicable records have been processed! ---")

    except Exception as e:
        print(f"\nAn unexpected error occurred during the main process: {e}")
    
    finally:
        print("\nAutomation finished. Closing browser in 5 seconds...")
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    main()