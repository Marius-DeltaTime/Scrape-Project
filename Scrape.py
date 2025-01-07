import requests
from bs4 import BeautifulSoup
import csv

# URL of the website to scrape
BASE_URL = "http://books.toscrape.com/"

def scrape_books(base_url):
    # Send an HTTP GET request to the website
    response = requests.get(base_url)
    if response.status_code != 200:
        print("Failed to fetch the webpage:", response.status_code)
        return

    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all book containers
    books = soup.find_all("article", class_="product_pod")
    if not books:
        print("No books found on the page.")
        return

    # List to store book data
    book_data = []

    # Extract details for each book
    for book in books:
        # Title
        title = book.h3.a["title"]

        # Price
        price = book.find("p", class_="price_color").text.strip()

        # Availability
        availability = book.find("p", class_="instock availability").text.strip()

        # Append the extracted details to the book_data list
        book_data.append({"Title": title, "Price": price, "Availability": availability})

    # Save the data to a CSV file
    save_to_csv(book_data)

def save_to_csv(book_data):
    # CSV file name
    filename = "books.csv"

    # Field names
    fields = ["Title", "Price", "Availability"]

    # Write data to CSV
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(book_data)

    print(f"Data saved to {filename}")

if __name__ == "__main__":
    scrape_books(BASE_URL)
