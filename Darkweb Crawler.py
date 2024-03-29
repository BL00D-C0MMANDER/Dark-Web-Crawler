import time
import requests
from stem import Signal
from stem.control import Controller
from bs4 import BeautifulSoup

# Set the number of links to crawl
num_links_to_crawl = 100

# Set the user agent to use for the request
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'

# Set the headers for the request
headers = {'User-Agent': user_agent}

# Initialize the controller for the Tor network
with Controller.from_port(port=9050) as controller:
    # Set the controller password
    controller.authenticate(password='mypassword')

    # Set the starting URL
    url = 'https://ahmia.fi/'

    # Initialize the visited set and the link queue
    visited = set()
    queue = [url]

    # Get the list of keywords to search for
    keywords = input('Enter a list of keywords to search for, separated by commas: ').split(',')

    # Crawl the links
    while queue:
        # Get the next link in the queue
        link = queue.pop(0)

        # Skip the link if it has already been visited
        if link in visited:
            continue

        # Set the new IP address
        controller.signal(Signal.NEWNYM)

        # Send the request to the URL
        response = requests.get(link, headers=headers)

        # Parse the response
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all links on the page
        links = soup.find_all('a')

        # Add any links that contain the keywords to the queue
        for a in links:
            href = a.get('href')
            if any(keyword in href for keyword in keywords):
                queue.append(href)

        # Add the link to the visited set
        visited.add(link)

        # Print the title and URL of the page
        print(soup.title.string, link)

        # Check if the number of visited links has reached the limit
        if len(visited) >= num_links_to_crawl:
            break

# Print the visited links
print('Visited links:')
for link in visited:
    print(link)
