from nltk import word_tokenize, pos_tag
import spacy
from type_utils import company_data, get_ticker
import re

#nltk.download('punkt')
#nltk.download('maxent_ne_chunker')
#nltk.download('words')

nlp = spacy.load("en_core_web_sm")


# Define a custom entity pattern
custom_patterns = []
for name in company_data.keys():
    label = {"label": "ORG", "pattern": name}
    custom_patterns.append(label)

# Add the custom patterns to the pipeline
ruler = nlp.add_pipe("entity_ruler")
ruler.add_patterns(custom_patterns)


def extract_company(text: str) -> str:
    text = re.sub(r"N(\d+)(.*)|('[a-zA-Z0-9]+)", "", text)
    doc = nlp(text)

    companies = []
    for ent in doc.ents:
        if ent.label_ == "ORG":
            ticker = get_ticker(ent.text)
            if ticker:
                companies.append(ticker)
            else:
                companies.append(ent.text)

    if "NGX" in companies and len(companies) > 1:
        companies.remove("NGX")

    companies = ','.join([comp for comp in companies])

    return companies