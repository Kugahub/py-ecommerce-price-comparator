from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

def scrape_powerbuy(driver, keyword, max_pages=10):
    import time
    all_products = []

    for page in range(1, max_pages + 1):
        url = f"https://www.powerbuy.co.th/th/search/{keyword}?page={page}"
        driver.get(url)

        try:
            wait = WebDriverWait(driver, 10)
            product_cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-sku]')))
        except:
            print(f"No products found on page {page}. Ending scrape.")
            break

        for card in product_cards:
            try:
                name = card.find_element(By.CSS_SELECTOR, 'h2 span:nth-of-type(2)').text
                price = card.find_element(By.CSS_SELECTOR, '.text-redPrice').text.replace('฿', '').replace(',', '').strip()
                link = card.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                all_products.append({
                    'title': name,
                    'price(THB)': float(price),
                    'link': "https://www.powerbuy.co.th" + link,
                    'source': 'PowerBuy'
                })
            except Exception as e:
                print("Skipping product:", e)

        print(f"✅ Collected {len(product_cards)} products from page {page}")
        time.sleep(1)

    return pd.DataFrame(all_products)



# if __name__ == "__main__":
#     from selenium import webdriver
#     from selenium.webdriver.chrome.options import Options

#     options = Options()
#     # options.add_argument('--headless')
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')

#     driver = webdriver.Chrome(options=options)
    
#     try:
#         df = scrape_powerbuy(driver, "smart watch")
#         print(df.head())
#     finally:
#         driver.quit()