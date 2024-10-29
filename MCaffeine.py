
#Import libraries
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Chrome options and Service
chrome_options = webdriver.ChromeOptions()
service = Service(executable_path="C:/Users/Kanika/anaconda3/Lib/site-packages/selenium/chromedriver.exe")


# Initialize WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)


driver.get('https://www.google.com/')
time.sleep(2)

wait = WebDriverWait(driver, 10)
search = wait.until(EC.element_to_be_clickable((By.NAME, "q")))

search.send_keys("mcaffeine")
time.sleep(2)

search.send_keys(Keys.ENTER)
time.sleep(2)


try:
    # Wait for the clickable link for "mcaffeine" in the search results
    clickable_element = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='v5yQqb']/a"))
    )
    print("Element found, attempting to click.")
    clickable_element.click()
    print("Element clicked successfully.")
except Exception as e:
    print("Error occurred:", e)

time.sleep(5)

clickable_element1 = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[7]/div[2]/div[3]/button[1]")))
clickable_element1.click()
time.sleep(2)

clickable_element2 = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/div[1]/div[2]/div/div/div/div[2]/a")))
clickable_element2.click()
time.sleep(5)

product_data = []

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to the bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Allow time for new products to load

    # Calculate new scroll height and compare with last height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break  # Break loop if no new products load
    last_height = new_height

# Now that all products are loaded, get product details
products = driver.find_elements(By.CLASS_NAME, "grid__item")
print(len(products))
# Loop to extract details of each product
for product in products:
    try:
        title = product.find_element(By.CLASS_NAME, "mm-product-title").text
        price = product.find_element(By.CLASS_NAME, "mmc-card-price").text
        description=product.find_element(By.CLASS_NAME, "mCaffeine__meta-tags").text
        review=product.find_element(By.CLASS_NAME, "product-reviews-ratings").text
        try:
            tag=product.find_element(By.CLASS_NAME, "sale-col").text
        except:
            continue
        product_data.append({'name': title, 'price': price,'description':description,'review':review})

    except:
        continue

df = pd.DataFrame(product_data)
# print(df)

# Save DataFrame to a CSV file
df.to_csv('mcaffeine.csv')