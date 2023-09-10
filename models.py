import json
import requests
from type_utils import max_sentiment

# put it in an environ shi
API_TOKEN = "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"
#model = "nickmuchi/deberta-v3-base-finetuned-finance-text-classification"
model = "nickmuchi/finbert-tone-finetuned-finance-topic-classification"

API_URL = f"https://api-inference.huggingface.co/models/{model}"
headers = {"Authorization": f"Bearer {API_TOKEN}"}


def query(headline, api):
    payload = {"inputs": headline}
    data = json.dumps(payload)
    response = requests.request("POST", api, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))


def topic(headline):

    model = "nickmuchi/finbert-tone-finetuned-finance-topic-classification"
    API_URL = f"https://api-inference.huggingface.co/models/{model}"
    data = query(headline, API_URL)

    sentiment_dict = {}
    for sentiment in data[0]:
        sentiment_dict[sentiment["label"]] = sentiment["score"]

    return max_sentiment(sentiment_dict)

def classification(headline):

    model = "nickmuchi/deberta-v3-base-finetuned-finance-text-classification"
    API_URL = f"https://api-inference.huggingface.co/models/{model}"
    data = query(headline, API_URL)

    sentiment_dict = {}
    for sentiment in data[0]:
        sentiment_dict[sentiment["label"]] = sentiment["score"]

    return max_sentiment(sentiment_dict)

print(topic(r"MTN Nigeria raises N125bn via commercial paper notes"))