from datetime import datetime
import re
import json
from rapidfuzz import process, fuzz
import pandas as pd


# load nigerian companies data
with open("company_data.json", "rb") as f:
    company_data = json.load(f)

headlines = pd.read_csv("headlines.csv").set_index("Date")

# convert date format to datetime obj
def convert_date(date_str: str) -> datetime:
    date_str = date_str.strip()
    date_obj = datetime.strptime(date_str, "%B %d, %Y")
    return date_obj

def clean_text(text: str) -> str:
    pattern = r"\\(.*)" # regex pattern to match strings after a unicode escape character.
    text_str = re.sub(pattern, "", text)    
    return text_str

# Return maximum sentiment of news headline
def max_sentiment(sentiment: dict) -> str:
    scores = list(sentiment.values())
    for key, value in sentiment.items():
        if value == max(scores):
            return key

# extract ticker from company name        
def get_ticker(name: str) -> str:
    choices = company_data.keys() # list of company names
    matched_comp = process.extractOne(name, choices, scorer=fuzz.token_set_ratio, score_cutoff=80)

    if matched_comp:
        ticker = company_data[matched_comp[0]]
        return ticker
    
    else:
        return None