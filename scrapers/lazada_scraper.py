import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def scrape_lazada(driver, keyword, max_products=200):
    products = []
    page = 1
    
    while len(products) < max_products:
        url = f"https://www.lazada.co.th/catalog/?page={page}&q={keyword}"
        driver.get(url)
        
        try:
            # Wait up to 10 seconds for product blocks to appear
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".Bm3ON"))
            )
        except:
            print(f"No items found on page {page}. Ending scrape.")
            break


        try:
            items = driver.find_elements(By.CSS_SELECTOR, 'div.Bm3ON[data-qa-locator="product-item"]')
            if not items:
                print(f"No items found on page {page}. Exiting scrape.")
                break

            for item in items:
                try:
                    title = item.find_element(By.CSS_SELECTOR, '.RfADt a').text.strip()
                    price = item.find_element(By.CSS_SELECTOR, '.aBrP0 span').text.strip()
                    link = item.find_element(By.TAG_NAME, "a").get_attribute("href")

                    products.append({
                        "title": title,
                        "price(THB)": float(price.replace("฿", "").replace(",", "")),
                        "link": link,
                        "source": "Lazada"
                    })

                    if len(products) >= max_products:
                        break
                except Exception:
                    continue  # Skip malformed product

        except NoSuchElementException:
            print(f"No products found on page {page}.")
            break

        page += 1

    df = pd.DataFrame(products)
    return df

# if __name__ == "__main__":
#     from selenium import webdriver
#     from selenium.webdriver.chrome.options import Options

#     options = Options()
#     options.add_argument('--headless')
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')

#     driver = webdriver.Chrome(options=options)
    
#     try:
#         df = scrape_lazada(driver, "smart watch")
#         print(df.head())
#     finally:
#         driver.quit()  # Ensure the driver is closed after scraping