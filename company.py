import spacy

nlp = spacy.load("en_core_web_sm")

text = "The GSK Exit: The grim realities, the abundant opportunities"

doc = nlp(text)

for ent in doc.ents:
    print(ent.text, ent.label_)

def extract_company(text: str) -> str:
    doc = nlp(text)

    companies = []
    for ent in doc.ents:
        if ent.label_ == "ORG":
            companies.append(ent.text)

    return companies

#print(extract_company("FBN Holdings employee sold N28.8 million worth of shares"))