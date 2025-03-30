import click
import pandas as pd
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

# Set up Chrome options
options = Options()
options.add_argument("--start-maximized")

# Initialize WebDriver
driver = webdriver.Chrome(options=options)

def save_to_csv(product_data, strain, saved_count=0):
    # Filename is based on the strain name
    filename = f"{strain}.csv"
    if not product_data:
        return saved_count

    if os.path.exists(filename) and os.stat(filename).st_size > 0:
        df = pd.read_csv(filename)
        df_new = pd.DataFrame(product_data)
        initial_count = len(df)
        df_combined = pd.concat([df, df_new]).drop_duplicates(subset=["Link"], keep="last")
        new_count = len(df_combined) - initial_count
        df_combined.to_csv(filename, index=False)
    else:
        df_new = pd.DataFrame(product_data)
        df_new.to_csv(filename, index=False)
        new_count = len(df_new)

    saved_count += new_count  # Update count for the current strain

    # Print when saved count is a multiple of 20
    if saved_count % 20 == 0:
        print(f"{saved_count} data saved for {strain}")

    return saved_count

def search_product(search_term):
    driver.get("https://www.amazon.com")
    try:
        search_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
        )
        search_box.send_keys(search_term)
        search_box.submit()
    except TimeoutException:
        print(f"Timeout while trying to search for {search_term}")
    
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.sg-col-20-of-24'))
    )

def scroll_down():
    for _ in range(5):
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(2)

def scrape_data(search_term, saved_count):
    product_data = []
    time.sleep(5)

    try:
        products = driver.find_elements(By.CSS_SELECTOR, 'div.s-result-item.s-asin')
        for product in products:
            try:
                title = product.find_element(By.CSS_SELECTOR, "h2.a-size-base-plus").text.encode("utf-8").decode("unicode_escape")
                #title = product.find_element(By.CSS_SELECTOR, "").text
                
                #title = title.encode("utf-8").decode("unicode_escape")

                try:
                    price_whole = product.find_element(By.CSS_SELECTOR, "span.a-price-whole").text
                    price_fraction = product.find_element(By.CSS_SELECTOR, "span.a-price-fraction").text
                    price = price_whole + "." + price_fraction
                except NoSuchElementException:
                    price = "Price not available"

                link = product.find_element(By.CSS_SELECTOR, "a.a-link-normal.s-no-outline").get_attribute("href")

                product_data.append({
                    "Product Type": search_term,
                    "Product Description": title,
                    "Price in dollars": price,
                    "Link": link,
                    "Date": time.strftime("%Y-%m-%d")
                })
                
                # Save data and update saved count for the current strain
                saved_count = save_to_csv(product_data, search_term, saved_count=saved_count)

            except NoSuchElementException:
                continue

    except TimeoutException:
        print(f"Timeout while loading search results for {search_term}")

    return saved_count

def go_to_next_page():
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.s-pagination-item.s-pagination-next'))
        )
        next_button.click()
        return True
    except (NoSuchElementException, ElementClickInterceptedException, TimeoutException):
        return False

def scrape_amazon_products(search_terms, num_pages):
    for search_term in search_terms:
        # Initialize a fresh saved_count for each strain
        saved_count = 0
        
        # Search for the product
        search_product(search_term)
        
        # Process each page and save data
        for page in range(num_pages):
            scroll_down()
            saved_count = scrape_data(search_term, saved_count)  # Pass current saved_count for this strain
            if not go_to_next_page():
                break
            time.sleep(5)
            
def get_search_terms(file_path):
    try:
        with open(file_path, 'r') as f:
            input = [line.strip() + " probiotics" for line in f.readlines()]
        return input
    except Exception as e:
        print(f"Error reading search terms file: {e}")
        return []

if __name__ == "__main__":
    search_terms_file = "missing_input.txt" 
    search_terms = get_search_terms(search_terms_file)

    num_pages = 5  
    scrape_amazon_products(search_terms, num_pages)

    driver.quit()
