import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import sys

def scrape_links(url, depth, visited=None, tree=None):
    """
    look at this nice nice docstring my dsc20 teacher would be so proud
    Recursively scrape links from a URL up to a given depth.

    Args:
        url (str): The starting URL to scrape.(company website or whatever)
        depth (int): The depth to which links should be scraped.(to make sure you don't get irrelevant stuff that's too distantly related)
        visited (set): A set of visited URLs to avoid revisiting. this is for the purposes of recursion,
        but you can also put sites you don't want(can't think of a case where you'd need to, though)
        tree (dict): A dictionary representing the current level of the link tree. this is also for the purposes of recursion

    Returns:
        dict: A tree-like dictionary structure of links.
    """
    if visited is None:
        visited = set()
    if tree is None:
        tree = {}

    if depth < 0 or url in visited:
        return tree

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except (requests.RequestException, ValueError):
        print(f"Failed to fetch URL: {url}")
        return tree

    visited.add(url)
    tree[url] = {}

    soup = BeautifulSoup(response.text, 'html.parser')

    for link in soup.find_all('a', href=True):
        href = link['href']
        full_url = urljoin(url, href)  
        parsed_url = urlparse(full_url)

        if parsed_url.scheme in ('http', 'https') and full_url not in visited:
            tree[url][full_url] = {}
            scrape_links(full_url, depth - 1, visited, tree[url])

    return tree


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python scrape_links.py <url> <max_depth>")
        sys.exit(1)

    starting_url = sys.argv[1]
    try:
        max_depth = int(sys.argv[2])
    except ValueError:
        print("Error: max_depth must be an integer.")
        sys.exit(1)

    link_tree = scrape_links(starting_url, max_depth)

    output_file = "scraped_links.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(link_tree, f, indent=2)

    print(f"Scraped links saved to {output_file}")
