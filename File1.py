import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_page(url):
    # Send a GET request to the URL and get the HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the product containers on the page
    products = soup.find_all('div', {'class': 's-result-item'})

    # Extract the required data for each product
    data = []
    for product in products:
        # Extract the product URL
        url_element = product.find('a', {'class': 'a-link-normal s-no-outline'})
        if url_element is not None:
            url = url_element['href']
        else:
            url = ''

        # Extract the product name
        name_element = product.find('h2', {'class': 'a-size-mini a-spacing-none a-color-base s-line-clamp-2'})
        if name_element is not None:
            name = name_element.text.strip()
        else:
            name = ''

        # Extract the product price
        price_element = product.find('span', {'class': 'a-price-whole'})
        if price_element is not None:
            price = price_element.text.strip()
        else:
            price = ''

        # Extract the product rating
        rating_element = product.find('span', {'class': 'a-icon-alt'})
        if rating_element is not None:
            rating = rating_element.text.split()[0]
        else:
            rating = ''

        # Extract the number of product reviews
        reviews_element = product.find('span', {'class': 'a-size-base', 'dir': 'auto'})
        if reviews_element is not None:
            reviews = reviews_element.text.strip().split()[0]
        else:
            reviews = ''

        # Add the extracted data to the list
        data.append([url, name, price, rating, reviews])

    # Return the extracted data as a pandas DataFrame
    return pd.DataFrame(data, columns=['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews'])


def scrape_pages(query, num_pages):
    # Define the base URL with the search query
    base_url = 'https://www.amazon.in/s?k=bags&ref=sr_pg_1'

    # Loop through the specified number of pages
    data = []
    for i in range(1, num_pages+1):
        # Construct the URL for the current page
        url = base_url.format(query, i)

        # Scrape the data from the current page
        page_data = scrape_page(url)

        # Add the scraped data to the list
        data.append(page_data)

    # Concatenate the scraped data from all pages into a single DataFrame
    return pd.concat(data, ignore_index=True)
query = 'bags'
num_pages = 20

data = scrape_pages(query, num_pages)
data.to_csv('amazon_bags.csv', index=False)
