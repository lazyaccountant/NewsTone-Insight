from nltk import word_tokenize, pos_tag
import spacy
import pandas as pd
from type_utils import company_data, get_ticker

#nltk.download('punkt')
#nltk.download('maxent_ne_chunker')
#nltk.download('words')

nlp = spacy.load("en_core_web_sm")

#text = r"Dangote Sugar, NASCON lead gainers to open September positive"


# Define a custom entity pattern
custom_patterns = []
for name in company_data.keys():
    label = {"label": "ORG", "pattern": name}
    custom_patterns.append(label)

# Add the custom patterns to the pipeline
ruler = nlp.add_pipe("entity_ruler")
ruler.add_patterns(custom_patterns)


def extract_company(text: str) -> str:
    doc = nlp(text)

    companies = []
    for ent in doc.ents:
        if ent.label_ == "ORG":
            ticker = get_ticker(ent.text)
            if ticker:
                companies.append(ticker)
            else:
                companies.append(ent.text)

    text = text.lower()
    words = word_tokenize(text)
    tagged_words = pos_tag(words)

    for i, word in enumerate(tagged_words):
        if word[-1] == "NNP":
            
            if i+1 < len(tagged_words) and word[-1] == tagged_words[i+1][-1]: # check if there are two consecutive noun phrases
                name = " ".join([word[0], tagged_words[i+1][0]]) # join NNP together
                if name not in companies:
                    ticker = get_ticker(name)
                    if ticker:
                        companies.append(ticker)
                    else:
                        companies.append(name)

            elif i+1 < len(tagged_words) and word[-1] != tagged_words[i+1][-1]: # check for single noun phrase
                name = word[0]
                if name not in companies:
                    ticker = get_ticker(name)
                    if ticker:
                        companies.append(ticker)
                    else:
                        companies.append(name)

    if "NGX" in companies and len(companies) > 1:
        companies.remove("NGX")

    return companies



df = pd.read_csv("headlines.csv").set_index("Date")

df["company"] = df["News"].apply(extract_company)

print(df)