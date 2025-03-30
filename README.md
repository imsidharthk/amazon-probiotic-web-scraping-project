# amazon-probiotic-web-scraping-project
Amazon Product Scraper

Overview

This project is an Amazon product scraper that automates the process of searching for products on Amazon, extracting relevant details, and saving them to a CSV file. The scraper utilizes Selenium to interact with Amazon's search interface, navigate through multiple pages, and collect product information.

Features

Automates product search on Amazon

Extracts product details such as:

Product description

Price

Product link

Date of extraction

Scrolls through search results for comprehensive data collection

Navigates multiple pages to extract more results

Saves the scraped data into a CSV file, avoiding duplicate entries

Technologies Used

Python: Core scripting language

Selenium: Web automation framework for interacting with Amazon

Pandas: Data handling and CSV management

Click: Command-line interaction

Installation

Prerequisites

Ensure you have the following installed:

Python (>=3.7)

Google Chrome browser

Chrome WebDriver

Setup

Clone this repository:


Install required dependencies:

pip install -r requirements.txt

Download and configure Chrome WebDriver:

Ensure the Chrome WebDriver version matches your Chrome browser version.

Place the WebDriver in the project directory or add it to your system PATH.

Usage

Prepare a text file (missing_input.txt) containing a list of search terms, one per line.

Run the script:

python scraper.py

The script will:

Read search terms from missing_input.txt.

Search for products on Amazon.

Extract relevant product details.

Save the data to a CSV file named after the search term.

Code Explanation

Key Functions

search_product(search_term): Searches for the given product on Amazon.

scroll_down(): Scrolls down the page to load more products.

scrape_data(search_term, saved_count): Extracts product details from search results.

save_to_csv(product_data, strain, saved_count=0): Saves extracted data to a CSV file, avoiding duplicates.

go_to_next_page(): Clicks the 'Next' button to navigate to the next search results page.

scrape_amazon_products(search_terms, num_pages): Orchestrates the scraping process for multiple search terms across multiple pages.

Output

A CSV file for each search term containing the following fields:

Product Type

Product Description

Price in Dollars

Link

Date

Limitations

Amazon may block automated requests after excessive usage.

CAPTCHA or bot detection may prevent scraping in some cases.

The script is optimized for Amazon's current layout, which may change over time.
