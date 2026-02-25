import requests
from bs4 import BeautifulSoup
import time

def parse_and_extract_rows(soup: BeautifulSoup):
    """
    Extract table rows from the parsed HTML.
    """
    header_row = soup.find('tr')
    if not header_row:
        return
        
    headers = [th.text.strip() for th in header_row.find_all('th')]
    teams = soup.find_all('tr', class_='team')
    
    for team in teams:
        row_dict = {}
        # Ensure we only zip columns that exist
        for header, col in zip(headers, team.find_all('td')):
            row_dict[header] = col.text.strip()
        yield row_dict

def scrape_all_pages():
    base_url = "https://www.scrapethissite.com"
    # Start with the initial relative path
    current_path = "/pages/forms/"
    all_data = []

    while True:
        url = f"{base_url}{current_path}"
        print(f"Fetching: {url}")
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract data from the current page
            page_data = list(parse_and_extract_rows(soup))
            all_data.extend(page_data)

            # --- Pagination Logic ---
            # We look for the 'Next' link which contains the '»' character
            # or specifically the aria-label="Next" attribute.
            next_link = soup.find('a', attrs={'aria-label': 'Next'})

            if next_link and 'href' in next_link.attrs:
                current_path = next_link['href']
                time.sleep(0.5)  # Be kind to the server!
            else:
                print("Reached the last page.")
                break
                
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    return all_data

# Example usage:
data = scrape_all_pages()
print(f"Total rows scraped: {len(data)}")