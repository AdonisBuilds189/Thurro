#!/usr/bin/env python3
"""
bse_announcements_downloader.py
Automates BSE corporate announcements PDF download with form filling
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

def download_bse_announcements():
    """Download BSE corporate announcements PDF with automated form filling"""
    
    # Chrome options for download handling
    chrome_options = Options()
    download_dir = os.path.join(os.getcwd(), "downloads")
    os.makedirs(download_dir, exist_ok=True)
    
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)
    
    try:
        # Navigate to BSE page
        url = "https://www.bseindia.com/stock-share-price/ashok-leyland-ltd/ashokley/500477/corp-announcements/"
        driver.get(url)
        
        # Wait for page to load
        time.sleep(3)
        
        # Fill form parameters as shown in image
        # From Date
        from_date = wait.until(EC.presence_of_element_located((By.ID, "FromDate")))
        from_date.clear()
        from_date.send_keys("01/01/2024")
        
        # To Date
        to_date = driver.find_element(By.ID, "ToDate")
        to_date.clear()
        to_date.send_keys("31/12/2024")
        
        # Select Category dropdown
        category_dropdown = Select(driver.find_element(By.ID, "ddlCategory"))
        category_dropdown.select_by_visible_text("All")
        
        # Select SubCategory if available
        try:
            subcategory_dropdown = Select(driver.find_element(By.ID, "ddlSubCategory"))
            subcategory_dropdown.select_by_visible_text("All")
        except:
            pass
        
        # Select Broadcast if available
        try:
            broadcast_dropdown = Select(driver.find_element(By.ID, "ddlBroadcast"))
            broadcast_dropdown.select_by_visible_text("All")
        except:
            pass
        
        # Click Submit button
        submit_btn = driver.find_element(By.ID, "btnSubmit")
        submit_btn.click()
        
        # Wait for results to load
        time.sleep(5)
        
        # Find and click PDF download button
        pdf_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'pdf') or contains(text(), 'PDF')]")))
        pdf_button.click()
        
        # Wait for download to complete
        time.sleep(10)
        
        print("PDF download initiated successfully!")
        print(f"Check downloads folder: {download_dir}")
        
    except Exception as e:
        print(f"Error during automation: {e}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    download_bse_announcements()
