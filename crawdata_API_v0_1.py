from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import date
import requests
import json

size_map = []
lastmod_time = date.today().strftime('%Y-%m-%d')  # Convert date to string

app = Flask(__name__)
CORS(app)
api = Api(app)


def crawl_data(url, base_url, visited_urls=set(), max_redirects=5, current_priority=1.0):
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

            for link in links:
                link_href = link.get('href')
                link_title = link.get('title')

                # Check if link_href is not empty, not equal to '#' or '/', not starting with 'mailto:',
                # has the same hostname as the base_url
                if link_href and link_href not in ['#', '/'] and not link_href.startswith('mailto:'):
                    absolute_url = urljoin(base_url, link_href)

                    # Parse the hostname of the absolute URL
                    parsed_url = urlparse(absolute_url)

                    if parsed_url.netloc == urlparse(base_url).netloc:
                        # Check if the URL hasn't been visited to avoid infinite loops
                        if absolute_url not in visited_urls:
                            print(link_title, ':', absolute_url,
                                  'current_priority:', current_priority)

                            # Round current_priority to 2 decimal places
                            current_priority = round(current_priority, 2)

                            size_map.append({
                                'loc': absolute_url,
                                'lastmod': lastmod_time,
                                'priority': current_priority  # Set priority value
                            })

                            visited_urls.add(absolute_url)

                            # Recursively crawl the linked page with decreased priority
                            crawl_data(absolute_url, base_url, visited_urls,
                                       max_redirects=max_redirects, current_priority=current_priority - 0.1)

        else:
            print(
                f"Failed to fetch the page. Status code: {response.status_code}")

    except requests.exceptions.TooManyRedirects:
        print(f"Too many redirects for URL: {url}")


class ApiCrawlData(Resource):
    def get(self, link_craw):
        crawl_data(link_craw, link_craw)
        return jsonify(size_map)

    def post(self, link_craw):
        # You can handle POST requests here if needed
        crawl_data(link_craw, link_craw)

        # Access JSON data from the request body using request.json
        data = request.json
        print("Received POST data:", data)

        return jsonify({"message": "POST request received successfully"})


# Allow both GET and POST requests for the '/api_crawl_data' endpoint
api.add_resource(ApiCrawlData, '/api_crawl_data', methods=["GET", "POST"])


if __name__ == '__main__':
    app.run(debug=True)

# Save the sitemap to a JSON file
with open('sitemap_api.json', 'w', encoding='utf-8') as json_file:
    json.dump(size_map, json_file, ensure_ascii=False, indent=2)