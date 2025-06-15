from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def fill_google_form_from_excel_selenium():
    """
    Fills a Google Form with data from an Excel file using Selenium directly.
    Assumes ChromeDriver is in your system's PATH environment variable.
    """
    df = pd.read_excel('data.xlsx')

    # ChromeDriver is expected to be in your system's PATH
    driver = webdriver.Chrome()

    form_url = 'https://forms.gle/qMFvYEouXZFPCtDB7'
    driver.get(form_url)
    time.sleep(3)  # Wait for the page to load

    for index, row in df.iterrows():
        # Fill out the form fields
        # Name Field
        name_field_locator = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'
        name_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, name_field_locator)))
        name_field.clear()
        name_field.send_keys(row['Name'])

        # Address Field
        address_field_locator = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div[2]/textarea'
        address_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, address_field_locator)))
        address_field.clear()
        address_field.send_keys(row['Address'])

        # Phone Number Field
        phone_field_locator = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'
        phone_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, phone_field_locator)))
        phone_field.clear()
        phone_field.send_keys(str(row['Phone Number']))

        # Highschool Field
        highschool_field_locator = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input'
        highschool_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, highschool_field_locator)))
        highschool_field.clear()
        highschool_field.send_keys(row['Highschool'])

        # GPA Field
        gpa_field_locator = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div/div[1]/input'
        gpa_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, gpa_field_locator)))
        gpa_field.clear()
        gpa_field.send_keys(str(row['Gpa']))

        # Select course radio button
        course = row['Course Interested']
        if course == 'Mechanical Engineering':
            course_radio_button_locator = '//*[@id="i34"]/div[3]/div'
        elif course == 'Computer Science':
            course_radio_button_locator = '//*[@id="i31"]/div[3]/div'
        elif course == 'Mechanical Science':
            course_radio_button_locator = '//*[@id="i37"]/div[3]/div'
        elif course == 'Data Science':
            course_radio_button_locator = '//*[@id="i40"]/div[3]/div'
        else:
            course_radio_button_locator = '//*[@id="i40"]/div[3]/div' #Default to Data Science

        course_radio_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, course_radio_button_locator)))
        course_radio_button.click()


        # Submit the form
        submit_button_locator = '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div'
        submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, submit_button_locator)))
        submit_button.click()
        time.sleep(2)  # Short wait

        # Wait and click the "Submit Another Response" link
        submit_another_button_locator = '//div[@class="c2gzEf"]/a'
        submit_another_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, submit_another_button_locator)))
        submit_another_button.click()


        print(f"Form submitted for row {index + 1}")

    driver.quit()
    print("Automation finished.")

if __name__ == "__main__":
    fill_google_form_from_excel_selenium()