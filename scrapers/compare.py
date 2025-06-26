from .lazada_scraper import scrape_lazada
from .powerbuy_scraper import scrape_powerbuy
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from datetime import datetime

def compare_prices(search_query):
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Connect to the selenium/standalone-chrome container
    driver = webdriver.Remote(
        command_executor="http://selenium:4444/wd/hub",
        options=options  # ✅ use only this
    )
    
    lazada_df = scrape_lazada(driver, search_query)
    powerbuy_df = scrape_powerbuy(driver, search_query)

    driver.quit()
    
    # Add source platform as a column if not already included
    lazada_df = lazada_df.append(powerbuy_df, ignore_index=True)
    combined_df = lazada_df

    # Ensure output folder exists
    output_dir = "/opt/airflow/output"
    os.makedirs(output_dir, exist_ok=True)

    # Export to Excel
    timestamp = datetime.now().strftime("%Y-%m-%d")
    filename = f"product_prices_{timestamp}.xlsx"
    output_path = os.path.join(output_dir, filename)
    combined_df.to_excel(output_path, index=False)

    print(f"[✔] Comparison file saved at {output_path}")
    return output_path  # For use in next task
