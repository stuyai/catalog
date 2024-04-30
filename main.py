from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Function to check if the size of the element is stable
def wait_for_stable_size(driver, xpath, timeout=10):
    old_size = 0
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            element = driver.find_element(By.XPATH, xpath)
            new_size = len(element.get_attribute('innerHTML'))
            if new_size == old_size:
                return True
            old_size = new_size
            time.sleep(1)  # wait for a second before checking again
        except:
            pass
    return False

# Setting up Chrome with Selenium
options = Options()
options.headless = True  # Enable headless mode
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get('https://stuyactivities.org/catalog')

    # Wait for the #root element to load completely
    if wait_for_stable_size(driver, "//*[@id='root']"):
        content = driver.page_source
        soup = BeautifulSoup(content, 'lxml')
        print(soup.prettify())
    else:
        print("Timed out waiting for the content to stabilize.")
finally:
    driver.quit()

