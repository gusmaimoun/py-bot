from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

ACCOUNT_EMAIL = "demopythoncapstone@gmail.com"
ACCOUNT_PASSWORD = "pythoncapstone123456"
PHONE = "0101010101"
RESUME_PATH = "C:\\Users\\gusta\\OneDrive\\Desktop\\Resume\\Gustavo Maimoun Resume.pdf"

def abort_application():
    # Click Close Button
    close_button = driver.find_element(By.CLASS_NAME,"artdeco-modal__dismiss")
    close_button.click()

    time.sleep(2)
    # Click Discard Button
    discard_button = driver.find_element(By.CLASS_NAME,"artdeco-modal__confirm-dialog-btn")
    discard_button.click()

# Optional - Automatically keep your chromedriver up to date.
chrome_driver_path = ChromeDriverManager().install()

# Optional - Keep the browser open if the script crashes.
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach",True)

service = ChromeService(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service,options=chrome_options)

driver.get(
    "https://www.linkedin.com/jobs/search/?currentJobId=3586148395&f_LF=f_AL&geoId=101356765&"
    "keywords=python&location=New+York+City%2C+New+York%2C+United+States&refresh=true")

# Click Reject Cookies Button
time.sleep(5)
try:
    reject_button = driver.find_element(By.CSS_SELECTOR,'button[action-type="DENY"]')
    reject_button.click()
except NoSuchElementException:
    print("Reject button not found or not necessary.")

# Click Sign in Button
time.sleep(2)
try:
    sign_in_button = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.LINK_TEXT,"Sign in")))
    driver.execute_script("arguments[0].click();",sign_in_button)
except ElementClickInterceptedException:
    print("Element click intercepted. Trying again.")
    time.sleep(2)
    driver.execute_script("arguments[0].click();",sign_in_button)
# Sign in
time.sleep(5)
email_field = driver.find_element(By.ID,"username")
email_field.send_keys(ACCOUNT_EMAIL)
password_field = driver.find_element(By.ID,"password")
password_field.send_keys(ACCOUNT_PASSWORD)
password_field.send_keys(Keys.ENTER)

# Get Listings
time.sleep(5)
all_listings = driver.find_elements(By.CSS_SELECTOR,".job-card-container--clickable")

# Apply for Jobs
for listing in all_listings:
    print("Opening Listing")
    listing.click()
    time.sleep(2)
    try:
        # Click Apply Button
        apply_button = driver.find_element(By.CSS_SELECTOR,".jobs-s-apply button")
        apply_button.click()

        # Insert Phone Number
        # Find an <input> element where the id contains phoneNumber
        time.sleep(5)
        phone = driver.find_element(By.CSS_SELECTOR,"input[id*=phoneNumber]")
        if phone.get_attribute("value") == "":
            phone.send_keys(PHONE)

        # Upload Resume
        upload_button = driver.find_element(By.CSS_SELECTOR,'input[type="file"]')
        upload_button.send_keys(RESUME_PATH)

        # Check the Submit Button
        submit_button = driver.find_element(By.CSS_SELECTOR,"footer button")
        if submit_button.get_attribute("data-control-name") == "continue_unify":
            abort_application()
            print("Complex application, skipped.")
            continue
        else:
            # Click Submit Button
            print("Submitting job application")
            submit_button.click()

        time.sleep(2)
        # Click Close Button
        close_button = driver.find_element(By.CLASS_NAME,"artdeco-modal__dismiss")
        close_button.click()

    except NoSuchElementException:
        abort_application()
        print("No application button, skipped.")
        continue

time.sleep(5)
driver.quit()
