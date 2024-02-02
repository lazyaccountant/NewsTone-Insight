import json
import requests
from type_utils import max_sentiment
import pandas as pd
import time
import streamlit as st
from dotenv import load_dotenv
import os

#load_dotenv()

#API_TOKEN = os.getenv("API_TOKEN")
API_TOKEN = st.secrets["API_TOKEN"]

headers = {"Authorization": f"Bearer {API_TOKEN}"}


def query(headline, api):
    payload = {"inputs": headline,
                "wait_for_model": "True"}
    data = json.dumps(payload)
    response = requests.request("POST", api, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))


def topic(headline):

    model = "nickmuchi/finbert-tone-finetuned-finance-topic-classification"
    API_URL = f"https://api-inference.huggingface.co/models/{model}"
    data = query(headline, API_URL)

    sentiment_dict = {}
    try:
        for sentiment in data[0]:
            sentiment_dict[sentiment["label"]] = sentiment["score"]

        return max_sentiment(sentiment_dict)
    except KeyError:
        time.sleep(1)
        topic(headline)
    

def classification(headline):

    model = "nickmuchi/deberta-v3-base-finetuned-finance-text-classification"
    API_URL = f"https://api-inference.huggingface.co/models/{model}"
    data = query(headline, API_URL)

    sentiment_dict = {}
    try:
        for sentiment in data[0]:
            sentiment_dict[sentiment["label"]] = sentiment["score"]

        return max_sentiment(sentiment_dict)
    except KeyError:
        time.sleep(1)
        classification(headline)