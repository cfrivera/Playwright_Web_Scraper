from playwright.sync_api import Playwright, sync_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

# Function to find tables in HTML
def get_table_rows(table):
    rows = []
    
    # Get the headers (column names) from the first row of the table
    headers = [header.text for header in table.find('tr').find_all('th')]
    
    # Iterate over the remaining rows of the table (tr = table row)
    for tr in table.find_all('tr')[1:]:
        # Create a new dictionary to store the data for this row
        row = {}
        
        # Add the values for each column to the row dictionary
        for header, cell in zip(headers, tr.find_all('td')):
            row[header] = cell.text
            
        # Append the completed row dictionary to the rows list
        rows.append(row)
    
    return rows # this is a list the contains dictionaries that = a table
def find_tables(soup):
    return [get_table_rows(table) for table in soup.find_all('table') if table.find('tr') is not None]

def find_text(child):
    # Extract and print the text content of the paragraph tag
    paragraph_text = ' '.join(child.stripped_strings)
    # paragraph_text = child.get_text(strip=True)
    print(paragraph_text)

def get_equation(soup):
    ...

def scrape_chapters(playwright: Playwright, url) -> None:
    global data
    last_chapter = False
    web_domain = 'https://www.accessengineeringlibrary.com'

    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    page.goto(url)

    time.sleep(2)

    # Get the HTML content from the page
    html_content = page.content()

    # Initialize next_url with a default value
    next_url = ''

    # Check if the class 'toc-pager__next' exists
    last_chapter_check = page.locator('.toc-pager__next nav--disabled') # why the dot?

    if last_chapter_check.is_visible():
        last_chapter = True
    else:
        # Get the href link from the 'toc-pager__next' class
        next_url_element = page.locator('.toc-pager__next')
        next_url = next_url_element.get_attribute('href')
        if next_url:
            next_url = web_domain + next_url
            print('not the last chapter')
        else:
            last_chapter = True
            print('last chapter :D You did it babe!!! xxx')

    # ---------------------
    context.close()
    browser.close()

    # ... (your other code)

    return next_url, last_chapter

def main():
    # Check if it's the first time and run accordingly
    last_chapter = False
    data = []
    url = 'https://www.accessengineeringlibrary.com/content/book/9781260011968/back-matter/appendix1' #start of textbook

    while last_chapter != True:
        with sync_playwright() as playwright:
            url, last_chapter = scrape_chapters(playwright, url)


main()