# AutoLankaScraper

AutoLankaScraper is a Python class used to scrape data from the AutoLanka website (https://auto-lanka.com). The extracted data includes name of the car, posted date, posted city, price, condition, year of manufacture, the link to the car details page. The data is returned as a JSON string.

## Requirements
* requests
* BeautifulSoup
* json
* re

## Additional information
* The script scrapes the following information for each result: name, link, year of manufacture, condition, price, posted on, and posted city.
* The posted on date is obtained by visiting the link for each result and scraping the information from the webpage.
* The code is written in Python 3.9.

## Usage
1. Install the required Python packages by running pip install -r requirements.txt in your terminal.
2. Create an instance of the AutoLankaScraper class, passing the search query as the first argument. You can also pass keyword arguments.
3. Call the `search` method on the AutoLankaScraper instance to initiate the search and scrape the data.

Example usage:
```
search_query = "cars"
scraper = AutoLankaScraper(search_query, model="honda")
results = scraper.search()
print(results)
```

Note: Make sure to replace the `model` parameter with the appropriate one.