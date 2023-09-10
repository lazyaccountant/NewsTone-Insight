import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from type_utils import *

urls = "https://nairametrics.com/category/market-news/page/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}


headline = {
        "Date": [],
        "News": []
    }

for i in range(1, 10):
    time.sleep(2)
    url = urls + str(i)
    req = requests.get(url, headers=headers)

    soup = BeautifulSoup(req.text, "html.parser")

    # Find the <article> tag
    article_tags = soup.find_all('article')

    
    for article in article_tags:
        content = article.find("div", class_="jeg_postblock_content")
        top_header = content.find("h2")
        header = content.find("h3")
        date_cont = content.find("div", class_="jeg_meta_date")

        if top_header:
            news = top_header.find("a")
            date = date_cont.find("a")
            if news.get_text() not in headline["News"]:
                news_text = clean_text(news.get_text())
                headline["News"].append(news_text)
                date_obj = convert_date(date.get_text())
                headline["Date"].append(date_obj)

        if header:
            news = header.find("a")
            date = date_cont.find("a")
            if news.get_text() not in headline["News"]:
                news_text = clean_text(news.get_text())
                headline["News"].append(news_text)
                date_obj = convert_date(date.get_text())
                headline["Date"].append(date_obj)
            


df = pd.DataFrame(headline)
df.set_index("Date")
df.to_csv("headlines.csv")
#print(df.head())
#print(len(headline["Date"]), len(headline["News"]))

#print(req.text)