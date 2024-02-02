from datetime import datetime
import json
from rapidfuzz import process, fuzz


# load nigerian companies data
with open("data/company_data.json", "rb") as f:
    company_data = json.load(f)

# convert date format to datetime obj
def convert_date(date_str: str) -> datetime:
    date_str = date_str.strip()
    date_obj = datetime.strptime(date_str, "%B %d, %Y")
    return datetime.strftime(date_obj, "%m/%d/%Y")

# Return maximum sentiment of news headline
def max_sentiment(sentiment: dict) -> str:
    scores = list(sentiment.values())
    for key, value in sentiment.items():
        if value == max(scores):
            return key

# extract ticker from company name        
def get_ticker(name: str) -> str:
    choices = company_data.keys() # list of company names
    matched_comp = process.extractOne(name, choices, scorer=fuzz.token_set_ratio, score_cutoff=85)

    if matched_comp:
        ticker = company_data[matched_comp[0]]
        return ticker
    
    else:
        return None
    
def remove_unicode(text: str) -> str:
    string_encode = text.encode("ascii", "ignore")
    string_decode = string_encode.decode()
    return string_decode