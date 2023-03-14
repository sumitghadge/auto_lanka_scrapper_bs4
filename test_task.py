import json
import re

import requests
from bs4 import BeautifulSoup


class AutoLankaScraper:
    def __init__(self, search_query, **kwargs):
        self.website = "https://auto-lanka.com"
        self.search_query = search_query
        self.regx_for_date_pattern = "\d{2}\s+\w{3}\s+\d{2}:\d{2}\s+(?:AM|PM)"

        if kwargs:
            for key, value in kwargs.items():
                self.search_query = self.search_query + "&{}={}".format(key, value)

    def scrape_data(self, div_tag):
        print("Scrapping work is going on...")

        item = {}
        script_tag = div_tag.find("script", {"type": "application/ld+json"})
        data = script_tag.text.replace("\n", "").replace("\r", "").strip()
        dict_of_info = json.loads(data.strip())

        name = dict_of_info["name"]
        link = dict_of_info["url"]
        year_of_manufacture = dict_of_info["modelDate"]
        condition = dict_of_info["itemCondition"]
        price = div_tag.find("div", {"class": "item-price black"}).text

        # To get exact information of posted date and time we need to open this block
        # if we don't need exact date and time we can definately skip this step and 
        # just grab the data from soup object only
        response_from_block = requests.get(link)
        soup_of_block = BeautifulSoup(response_from_block.content, "html.parser")
        div_of_block = soup_of_block.find(
            "div", {"id": "ctl00_ContentPlaceHolder1_divCarDetails"}
        )
        posted_on = div_of_block.find("span").text
        posted_on = posted_on[
            re.search(self.regx_for_date_pattern, posted_on).span()[0] :
        ]
        posted_city = posted_on[
            re.search(self.regx_for_date_pattern, posted_on).span()[1] + 1 :
        ].split(",")[0]

        item["name"] = name
        item["posted_on"] = posted_on
        item["posted_city"] = posted_city
        item["price"] = price
        item["condition"] = condition
        item["year_of_manufacture"] = year_of_manufacture
        item["link"] = link

        return item

    def search(self):
        url = f"{self.website}/Default.aspx?qry={self.search_query}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        no_search_found = [
            h4
            for h4 in soup.find_all("h4")
            if "Sorry, no results found - try a different search." in h4.text
        ]

        if no_search_found:
            return json.dumps("No results found")

        list_of_results = []
        for a_tag in soup.find_all("a", href=True):
            div_tag = a_tag.find("div", {"class": "avdt-item row"})
            if div_tag:
                dict_of_result = {}
                data = self.scrape_data(div_tag)
                dict_of_result["overview"] = data
                list_of_results.append(dict_of_result)
                if len(list_of_results) == 10:
                    break

        print("Scrapping completed!!!")
        return json.dumps(list_of_results, indent=4)


search_query = "cars"
scraper = AutoLankaScraper(search_query, model="honda")
results = scraper.search()
print(results)
