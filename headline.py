import requests
from lxml import html
import time
from xpaths import *
from type_utils import *


def scrape_news(category: str = "Company"):
    """
    Scrape news headline from nairametrics website
    """

    urls = {
        "Company": "https://nairametrics.com/category/industries/latest-nigerian-company-news/page/",
        "Market": "https://nairametrics.com/category/market-news/page/"
    }
    #urls = "https://nairametrics.com/category/market-news/page/"
    #urls = "https://nairametrics.com/category/industries/latest-nigerian-company-news/page/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }

    headline = {} # Empty dict to store news headline and date

    # loop over three news website pages
    for i in range(1, 3):
        time.sleep(1)
        url = urls[category] + str(i)
        req = requests.get(url, headers=headers)
        parsed_content = html.fromstring(req.content) # Parse HTML content using lxml

        if i == 1: # retrieve top headlines from the first page only
            headline["Date"] = parsed_content.xpath(main_date_path)
            headline["News"] = parsed_content.xpath(main_headline_path)

            headline["Date"] = headline["Date"] + parsed_content.xpath(top_date_path)
            headline["News"] = headline["News"] + parsed_content.xpath(top_headline_path)

        headline["Date"] = headline["Date"] + parsed_content.xpath(date_path) # extract data using xpath
        headline["News"] = headline["News"] + parsed_content.xpath(headline_path)

    headline["News"] = [remove_unicode(news) for news in headline["News"]]

    return headline


if __name__ == "__main__":
    headline = scrape_news(category="Company")
    print(headline["News"])