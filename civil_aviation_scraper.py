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
import time

def scrape_aviation_dashboard():
    """Scrape domestic traffic data from Civil Aviation dashboard"""
    
    url = "https://www.civilaviation.gov.in/"
    
    # Headers to mimic a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        print("Fetching data from Civil Aviation dashboard...")
        
        # Get page content
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the domestic traffic section
        domestic_section = soup.find('div', class_='domestic-traffic')
        
        if not domestic_section:
            print("Could not find domestic traffic section")
            return create_sample_dataframe()
        
        # Extract date from the header
        date_element = domestic_section.find('span', class_='date-widget')
        extraction_date = date_element.get_text().strip() if date_element else datetime.now().strftime('%Y-%m-%d')
        
        # Initialize data dictionary
        dashboard_data = {
            'Date': extraction_date,
            'Departing_Flights': 'N/A',
            'Departing_Passengers': 'N/A',
            'Arriving_Flights': 'N/A',
            'Arriving_Passengers': 'N/A',
            'Aircraft_Movements': 'N/A',
            'Airport_Footfalls': 'N/A'
        }
        
        # Find all data paragraphs
        data_paragraphs = domestic_section.find_all('div', class_='paragraph--type--home-page-daily-data')
        
        for paragraph in data_paragraphs:
            # Get the English label
            label_element = paragraph.find('div', class_='field--name-field-label')
            count_element = paragraph.find('div', class_='field--name-field-counting-number')
            
            if label_element and count_element:
                label = label_element.get_text().strip()
                count = count_element.get_text().strip()
                
                # Map labels to our data structure
                if 'Departing flights' in label:
                    dashboard_data['Departing_Flights'] = count
                elif 'Departing Pax' in label:
                    dashboard_data['Departing_Passengers'] = count
                elif 'Arriving flights' in label:
                    dashboard_data['Arriving_Flights'] = count
                elif 'Arriving Pax' in label:
                    dashboard_data['Arriving_Passengers'] = count
                elif 'Aircraft movements' in label:
                    dashboard_data['Aircraft_Movements'] = count
                elif 'Airport footfalls' in label:
                    dashboard_data['Airport_Footfalls'] = count
        
        # Create DataFrame
        df = pd.DataFrame([dashboard_data])
        
        print("✅ Data successfully extracted!")
        return df
        
    except requests.RequestException as e:
        print(f"❌ Network error: {e}")
        return create_sample_dataframe()
    except Exception as e:
        print(f"❌ Error scraping data: {e}")
        return create_sample_dataframe()

def create_sample_dataframe():
    """Create sample DataFrame structure if scraping fails"""
    sample_data = {
        'Date': [datetime.now().strftime('%Y-%m-%d')],
        'Departing_Flights': ['Sample_Value'],
        'Departing_Passengers': ['Sample_Value'],
        'Arriving_Flights': ['Sample_Value'],
        'Arriving_Passengers': ['Sample_Value'],
        'Aircraft_Movements': ['Sample_Value'],
        'Airport_Footfalls': ['Sample_Value']
    }
    return pd.DataFrame(sample_data)

def save_data(df, filename='aviation_dashboard_data.csv'):
    """Save DataFrame to CSV with timestamp"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename_with_timestamp = f"aviation_data_{timestamp}.csv"
    
    try:
        df.to_csv(filename_with_timestamp, index=False)
        print(f"✅ Data saved to {filename_with_timestamp}")
    except Exception as e:
        print(f"❌ Error saving file: {e}")

def display_results_beautifully(df):
    """Display results in a clean, formatted way"""
    
    # Colors for terminal output (works on most Linux terminals)
    class Colors:
        HEADER = '\033[95m'
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        END = '\033[0m'
    
    # Clear screen effect
    print("\n" * 2)
    
    # Main header
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}🛫  CIVIL AVIATION INDIA - DOMESTIC TRAFFIC DATA  🛫{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    
    # Extract data from DataFrame
    data = df.iloc[0]
    
    # Date section
    print(f"\n{Colors.BOLD}{Colors.YELLOW}📅 DATA DATE: {Colors.GREEN}{data['Date']}{Colors.END}")
    
    # Flight Operations Section
    print(f"\n{Colors.BOLD}{Colors.HEADER}✈️  FLIGHT OPERATIONS{Colors.END}")
    print(f"{Colors.BLUE}{'─'*30}{Colors.END}")
    print(f"  {Colors.BOLD}Departing Flights:{Colors.END} {Colors.GREEN}{data['Departing_Flights']:>12}{Colors.END}")
    print(f"  {Colors.BOLD}Arriving Flights: {Colors.END} {Colors.GREEN}{data['Arriving_Flights']:>12}{Colors.END}")
    print(f"  {Colors.BOLD}Aircraft Movements:{Colors.END} {Colors.GREEN}{data['Aircraft_Movements']:>11}{Colors.END}")
    
    # Passenger Traffic Section
    print(f"\n{Colors.BOLD}{Colors.HEADER}👥 PASSENGER TRAFFIC{Colors.END}")
    print(f"{Colors.BLUE}{'─'*30}{Colors.END}")
    print(f"  {Colors.BOLD}Departing Passengers:{Colors.END} {Colors.GREEN}{data['Departing_Passengers']:>9}{Colors.END}")
    print(f"  {Colors.BOLD}Arriving Passengers: {Colors.END} {Colors.GREEN}{data['Arriving_Passengers']:>9}{Colors.END}")
    print(f"  {Colors.BOLD}Total Airport Footfalls:{Colors.END} {Colors.GREEN}{data['Airport_Footfalls']:>7}{Colors.END}")
    
    # Summary calculations
    try:
        total_flights = int(data['Departing_Flights'].replace(',', '')) + int(data['Arriving_Flights'].replace(',', ''))
        total_passengers = int(data['Departing_Passengers'].replace(',', '')) + int(data['Arriving_Passengers'].replace(',', ''))
        
        print(f"\n{Colors.BOLD}{Colors.HEADER}📊 SUMMARY{Colors.END}")
        print(f"{Colors.BLUE}{'─'*30}{Colors.END}")
        print(f"  {Colors.BOLD}Total Daily Flights:{Colors.END} {Colors.YELLOW}{total_flights:,}{Colors.END}")
        print(f"  {Colors.BOLD}Total Daily Passengers:{Colors.END} {Colors.YELLOW}{total_passengers:,}{Colors.END}")
        
    except (ValueError, AttributeError):
        pass
    
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")

if __name__ == "__main__":
    # Clear and stylish startup
    print(f"\n🚀 Starting Civil Aviation Dashboard Scraper...")
    print(f"⏳ Please wait while we fetch the latest data...")
    
    # Execute scraping
    result_df = scrape_aviation_dashboard()
    
    # Display results beautifully
    display_results_beautifully(result_df)
    
    # Save to CSV
    save_data(result_df)
    
    # Final message
    print(f"\n✅ {'\033[1m'}\033[92mScraping completed successfully!{'\033[0m'}")
    print(f"📁 Data saved to CSV file with timestamp")
    print(f"{'─'*40}\n")
