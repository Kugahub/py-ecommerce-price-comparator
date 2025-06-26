
from selenium.webdriver.common.by import By
import pandas as pd
import time

def scrape_ebay(driver, search_query):
    driver.get(f"https://www.ebay.com/sch/i.html?_nkw={search_query}")
    time.sleep(5)  # Let JS finish

    items = driver.find_elements(By.CSS_SELECTOR, "li.s-item")
    data = []

    for item in items:
        try:
            title_el = item.find_element(By.CSS_SELECTOR, "div.s-item__title span")
            price_el = item.find_element(By.CSS_SELECTOR, "span.s-item__price")
            title = title_el.text.strip()
            price = price_el.text.strip()

            if title and price:
                data.append({
                    "platform": "eBay",
                    "name": title,
                    "price": price,
                })

        except:
            continue

    return pd.DataFrame(data)

# # Test run
# if __name__ == "__main__":
#     df = scrape_ebay("cloth")
#     print(df.head())
