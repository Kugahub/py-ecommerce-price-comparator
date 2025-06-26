# 🛒 E-commerce Price Comparison Pipeline

This project is a **data pipeline for scraping product prices** from Thai e-commerce websites, comparing them, and **automatically uploading the results to Google Drive** as an Excel file.

### ✅ Features

- Scrapes prices from:
  - Lazada
  - eBay
  - Power Buy (1 page limit)
- Uses Selenium via remote Chrome container (`selenium/standalone-chrome`)
- Runs daily via Apache Airflow
- Outputs merged results in Excel, sorted by price
- Uploads the file to a specified folder in Google Drive

---

## 📁 Project Structure

```
.
├── dags/
│   ├── scrape_compare_upload.py        # Main Airflow DAG
├── gfrive_uploader/
│   ├── upload_to_gdrive.py             # Utility for uploading to Google Drive
├── output/                             # Excel output files (mounted)
├── creds/
│   └── service_account.json            # GDrive API credentials
└── scrapers/
│   ├── lazada_scraper.py
│   ├── ebay_scraper.py
│   ├── powerbuy_scraper.py
│   └── compare.py                      # Merges and exports results
│
├── Dockerfile                          # Airflow version + pip requirements
├── docker-compose.yml                  # Services: Airflow, Selenium Chrome
└── requirements.txt                    # Python dependencies
```

---

## 🚀 Quick Start

### 1. Prepare environment variables
Copy the template .env file and update the values as needed:
```bash
cp .env_template .env
```
💡 Edit .env to set things like your Google Drive folder ID

### 2. Start the system
Build and run the containers:
```bash
docker-compose up -d --build
```

Visit Airflow UI at: [http://localhost:8080](http://localhost:8080)

Default login:  
- **Username:** `airflow`  
- **Password:** `airflow`

---

## ⚙️ Configuration

You can change the product to search by modifying the `search_query` in:
```python
# dags/scrape_compare_upload.py
search_query = "smart watch"
```
or while manually executing DAGs with config:
```
{"search_query":"smart watch"}
```

---

## 🧪 Sample Output

Excel file will be named:
```
product_prices_YYYY-MM-DD.xlsx
```
And uploaded to the specified Google Drive folder.

Each row includes:
- Product name
- Price (float)
- Product link
- Source (Lazada, Power Buy)

---

## 🛠 Tech Stack

- Apache Airflow
- Python + Selenium
- Pandas
- Google Drive API (via `pydrive2`)
- Docker / docker-compose

---

## 🧼 Notes

- PowerBuy currently supports scraping only the first page, limiting the maximum number of products retrieved to 50..
- Shopee was avoided due to aggressive bot protection (JavaScript rendering + CAPTCHA).

---