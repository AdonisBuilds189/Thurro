#!/usr/bin/env python3
"""
civil_aviation_scraper.py
Scrapes domestic traffic data from Civil Aviation Government dashboard
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import re

def scrape_aviation_dashboard():
    """Scrape domestic traffic data from Civil Aviation dashboard"""
    
    url = "https://www.civilaviation.gov.in/"
    
    try:
        # Get page content
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find dashboard section - look for domestic traffic data
        dashboard_data = {}
        
        # Add current date
        dashboard_data['Date'] = datetime.now().strftime('%Y-%m-%d')
        
        # Look for data points in dashboard - adjust selectors based on actual HTML
        data_selectors = [
            {'name': 'Passengers', 'selector': '.passenger-count'},
            {'name': 'Flights', 'selector': '.flight-count'},
            {'name': 'Cargo', 'selector': '.cargo-count'},
            {'name': 'Aircraft_Movement', 'selector': '.aircraft-movement'},
            {'name': 'Route', 'selector': '.route-count'},
            {'name': 'Performance', 'selector': '.performance-metric'}
        ]
        
        # Extract data points
        for item in data_selectors:
            element = soup.select_one(item['selector'])
            if element:
                # Extract numeric value
                value = re.findall(r'[\d,]+', element.get_text())
                dashboard_data[item['name']] = value[0] if value else 'N/A'
            else:
                dashboard_data[item['name']] = 'N/A'
        
        # Create DataFrame
        df = pd.DataFrame([dashboard_data])
        
        return df
        
    except Exception as e:
        print(f"Error scraping data: {e}")
        
        # Return sample DataFrame structure if scraping fails
        sample_data = {
            'Date': [datetime.now().strftime('%Y-%m-%d')],
            'Passengers': ['Sample_Value'],
            'Flights': ['Sample_Value'],
            'Cargo': ['Sample_Value'],
            'Aircraft_Movement': ['Sample_Value'],
            'Route': ['Sample_Value'],
            'Performance': ['Sample_Value']
        }
        return pd.DataFrame(sample_data)

if __name__ == "__main__":
    # Execute scraping
    result_df = scrape_aviation_dashboard()
    
    # Display results
    print("Domestic Traffic Dashboard Data:")
    print(result_df)
    
    # Save to CSV
    result_df.to_csv('aviation_dashboard_data.csv', index=False)
    print("\nData saved to aviation_dashboard_data.csv")
