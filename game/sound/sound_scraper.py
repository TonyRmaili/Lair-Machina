import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Fetch the webpage using requests (this is just for analysis, not interaction)
url = 'https://loudme.ai/ai-music-generator'
response = requests.get(url)

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Locate the Description text area by its id or name (you need to inspect to find the actual id or name)
description_area = soup.find('textarea', {'id': 'description'})  # Replace with actual id from inspect
if description_area:
    print("Description text area found!")
    print(description_area)

# Locate the Create button (replace with actual class or id from inspect)
create_button = soup.find('button', {'class': 'coco-btn css-cyxjdm coco-btn-primary coco-btn-lg coco-btn-block flex items-center font-semibold antd_primaryButton__etKoH'})
if create_button:
    print("Create button found!")
    print(create_button)

# Initialize the WebDriver (Make sure ChromeDriver is properly set up)
driver = webdriver.Chrome()  # Replace with actual path to ChromeDriver

# Open the page
driver.get(url)

# Locate the "Description" text area using its id (replace 'description-field' with the actual id or name)
description_area = driver.find_element(By.ID, 'description')  # Use By.ID or other locator strategy
description_area.send_keys("Battle music with fantasy role playing game theme")  # Fill in the text

# Locate the "Create" button by its class or id (replace 'create-button' with the actual id or class)
create_button = driver.find_element(By.CSS_SELECTOR, '.coco-btn.css-cyxjdm.coco-btn-primary.coco-btn-lg.coco-btn-block.flex.items-center.font-semibold.antd_primaryButton__etKoH')
create_button.click()  # Click the create button


input("Press Enter to close the browser...")

# Close the browser window when done
driver.quit()
