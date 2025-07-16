import csv
import os
import pandas as pd  # Import pandas for Excel operations
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def scrape_google_location(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    
    driver.get(url)

    try:
        review_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "F7nice"))
        )
        title_element = driver.find_element(By.CSS_SELECTOR, "h1.DUwDvf.lfPIob")
        title = title_element.text.strip()
        rating_span = review_div.find_element(By.CSS_SELECTOR, "span[aria-hidden='true']")
        rating = rating_span.text.strip()
        reviews_span = review_div.find_element(By.CSS_SELECTOR, "span[aria-label*='reviews']")
        reviews = reviews_span.text.strip()
        reviews_numeric = ''.join(filter(str.isdigit, reviews))

        return {
            'Title': title,
            'Rating': rating,
            'Reviews': reviews_numeric
        }

    except TimeoutException as e:
        print(f"Timeout waiting for elements: {e}")
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

    return None

# Define the URLs directly in the script
urls = [
    "https://maps.app.goo.gl/3UVNkq3U927Uhiyi7",
    "https://maps.app.goo.gl/GHUrRW4nCRs2Zudw9",
    "https://maps.app.goo.gl/pzNcAZQRYR3beZXy5",
    "https://maps.app.goo.gl/RXUYs5gdELbxft31A",
    "https://maps.app.goo.gl/jvhqkyi3TUMFbQEy9",
    "https://maps.app.goo.gl/FV8Ba5mH41usPkUh8",
    "https://maps.app.goo.gl/6EpFzekVAvybFVUV7",
    "https://maps.app.goo.gl/mM319mohes7k8beV8",
    "https://maps.app.goo.gl/eBhzhGdoCuYPt4q6A",
    "https://maps.app.goo.gl/hgSkAMhAatw4MxyQ7",
    "https://maps.app.goo.gl/ZLwKTH3TkFgkvn9A7",
    "https://maps.app.goo.gl/d4vN7k2qbKPuLavD6"
]

# Scrape data for each link
output_data = []
for link in urls:
    print(f"Scraping data for: {link}")
    data = scrape_google_location(link)
    if data:
        # Add a timestamp column with date only in dd-mm-yyyy format
        timestamp = datetime.now().strftime('%d-%m-%Y')
        output_data.append([timestamp, data['Title'], data['Rating'], data['Reviews']])

# Create a DataFrame from the output data
df = pd.DataFrame(output_data, columns=["Timestamp", "Title", "Rating", "Reviews"])

# Output file path
output_excel_file = r"D:\Beautiful Soup\GetfromGoogleDC.xlsx"

# Save the DataFrame to an Excel file
df.to_excel(output_excel_file, index=False)

print("DONE")
