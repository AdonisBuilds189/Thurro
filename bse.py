from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pdfplumber
import pandas as pd
import time
import os

# --- Constants ---
PDF_FILE = "downloaded_report.pdf"
EXCEL_FILE = "converted_report.xlsx"
BASE_URL = "https://www.bseindia.com"

# --- Setup Selenium Driver (Headless Chrome) ---
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 15)

# --- Step 1: Load the Page ---
driver.get(f"{BASE_URL}/stock-share-price/ashok-leyland-ltd/ashokley/500477/corp-announcements/")
time.sleep(3)

# --- Step 2: Fill Date Fields ---
from_input = wait.until(EC.presence_of_element_located((By.ID, "txtFromDt")))
to_input = wait.until(EC.presence_of_element_located((By.ID, "txtToDt")))
driver.execute_script("arguments[0].value='22/04/2025';", from_input)
driver.execute_script("arguments[0].value='22/07/2025';", to_input)

# --- Step 3: Select Category & Subcategory ---
Select(wait.until(EC.element_to_be_clickable((By.ID, "ddlPeriod")))).select_by_visible_text("Company Update")
time.sleep(2)
Select(wait.until(EC.element_to_be_clickable((By.ID, "ddlsubcat")))).select_by_visible_text("Monthly Business Updates")

# --- Step 4: Click Submit ---
submit_btn = wait.until(EC.element_to_be_clickable((By.ID, "btnSubmit")))
submit_btn.click()
print("🚀 Submitted form with filters.")
time.sleep(5)

# --- Step 5: Find First <a href="...pdf"> Link ---
pdf_link = None
pdf_anchors = driver.find_elements(By.XPATH, "//a[contains(@class, 'tablebluelink') and contains(@href, '.pdf')]")

for tag in pdf_anchors:
    href = tag.get_attribute("href")
    if href.lower().endswith(".pdf"):
        pdf_link = BASE_URL + href if href.startswith("/") else href
        break

if not pdf_link:
    print("❌ NO PDF link found in filtered result. Try a different subcategory.")
    driver.quit()
    exit()

print(f"📥 PDF found: {pdf_link}")

# --- Step 6: Create Authenticated Session from Selenium Cookies ---
session = requests.Session()
for cookie in driver.get_cookies():
    session.cookies.set(cookie['name'], cookie['value'])

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": BASE_URL
}

# --- Step 7: Download the file using AUTHENTICATED session ---
res = session.get(pdf_link, headers=headers)

if res.headers.get("Content-Type") != "application/pdf":
    print("❌ Server did not return a valid PDF file.")
    with open("debug_response.html", "w", encoding="utf8") as f:
        f.write(res.text)
    print("📄 Saved debug response as 'debug_response.html'")
    driver.quit()
    exit()

with open(PDF_FILE, "wb") as f:
    f.write(res.content)

print(f"✅ PDF successfully downloaded: {PDF_FILE}")
driver.quit()

# --- Step 8: Convert PDF ➝ Excel ---
print("📊 Converting PDF to Excel table...")

df_list = []
try:
    with pdfplumber.open(PDF_FILE) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                df = pd.DataFrame(table[1:], columns=table[0])
                df_list.append(df)

    if df_list:
        final_df = pd.concat(df_list, ignore_index=True)
        final_df.to_excel(EXCEL_FILE, index=False)
        print(f"✅ Excel file created: {EXCEL_FILE}")
    else:
        print("⚠️ WARNING: No tabular data found inside the PDF.")
except Exception as e:
    print("❌ Failed to convert PDF:", e)
