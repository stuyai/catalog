import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv

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

def scrape_page(url):
    driver.get(url)
    if wait_for_stable_size(driver, "//*[@id='root']"):
        return driver.page_source
    else:
        print("Timed out waiting for the content to stabilize.")
        return ""

# Setup Chrome with Selenium
options = Options()
options.headless = True  # Enable headless mode
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

base_url = 'https://stuyactivities.org'

clubs = {}
# Open and read the CSV file
with open("./data/clubs.csv", mode='r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        club_name = row['Club Name'].strip()
        link = row['Link'].strip()
        clubs[club_name] = link	

try:
    for club_name, club_path in clubs.items():
        # Create directories for each club
        club_dir = f'./data/{club_name}'
        os.makedirs(club_dir, exist_ok=True)

        # Scrape main club page
        main_html = scrape_page(f'{base_url}{club_path}')
        with open(f'{club_dir}/main.txt', 'w', encoding='utf-8') as file:
            file.write(main_html)

        # Scrape charter page
        charter_html = scrape_page(f'{base_url}{club_path}/charter')
        with open(f'{club_dir}/charter.txt', 'w', encoding='utf-8') as file:
            file.write(charter_html)

        # Scrape members page
        members_html = scrape_page(f'{base_url}{club_path}/members')
        with open(f'{club_dir}/members.txt', 'w', encoding='utf-8') as file:
            file.write(members_html)
finally:
    driver.quit()

