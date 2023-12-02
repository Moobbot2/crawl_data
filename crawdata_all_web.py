import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def crawl_data(url, visited_urls=set()):
    # Send an HTTP request to the specified URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract data from the parsed HTML (modify this part based on your needs)
        # For example, let's extract all the links on the page
        links = soup.find_all('a')
        list_link = []
        
        for link in links:
            link_href = link.get('href')

            # Check if link_href is not empty and not equal to '#' or '/'
            if link_href and link_href not in ['#', '/'] and link_href not in list_link:
                list_link.append(link_href)
                absolute_url = urljoin(url, link_href)

                # Check if the URL hasn't been visited to avoid infinite loops
                if absolute_url not in visited_urls:
                    print(absolute_url)
                    visited_urls.add(absolute_url)

                    # Recursively crawl the linked page
                    crawl_data(absolute_url, visited_urls)

    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")

# Replace 'https://example.com' with the URL you want to start crawling
crawl_data('https://cvgmall.com')
