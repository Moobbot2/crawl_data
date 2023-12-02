import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

size_map = []

def crawl_data(url, visited_urls=set(), max_redirects=5):
    try:
        # Send an HTTP request to the specified URL with a maximum number of redirects
        response = requests.get(url, allow_redirects=True)

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
                link_title = link.get('title')

                # Check if link_href is not empty, not equal to '#' or '/', and not starting with 'mailto:'
                if link_href and link_href not in ['#', '/'] and not link_href.startswith('mailto:'):
                    list_link.append({
                        'url': link_href,
                        'title': link_title
                    })
                    size_map.append({
                        'loc': link_href,
                        'lastmod': time.time(),
                        'priority': ''  # You need to decide on the priority value
                    })
                    absolute_url = urljoin(url, link_href)

                    # Check if the URL hasn't been visited to avoid infinite loops
                    if absolute_url not in visited_urls:
                        print(link_title, ':', absolute_url)
                        visited_urls.add(absolute_url)

                        # Recursively crawl the linked page
                        crawl_data(absolute_url, visited_urls, max_redirects=max_redirects - 1)

        else:
            print(f"Failed to fetch the page. Status code: {response.status_code}")

    except requests.exceptions.TooManyRedirects:
        print(f"Too many redirects for URL: {url}")

# Replace 'https://example.com' with the URL you want to start crawling
crawl_data('https://cvgmall.com')
