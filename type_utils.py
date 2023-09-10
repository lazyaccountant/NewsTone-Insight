from datetime import datetime
import re


def convert_date(date_str: str) -> datetime:
    date_str = date_str.strip()
    date_obj = datetime.strptime(date_str, "%B %d, %Y")
    return date_obj

def clean_text(text: str) -> str:
    pattern = r"\\(.*)"
    text_str = re.sub(pattern, "", text)    
    return text_str

def max_sentiment(sentiment: dict) -> str:
    scores = list(sentiment.values())
    for key, value in sentiment.items():
        if value == max(scores):
            return key