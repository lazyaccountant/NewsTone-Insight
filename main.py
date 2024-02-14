import streamlit as st
import pandas as pd
from models import topic, classification
from company import extract_company

# Website Header
st.title("News:green[Tone] In:red[sight]📰")

# Separate webpage into two tabs
tab1, tab2 = st.tabs(["NewsTone", "News Headlines"])

with tab1:
    query = st.text_input(
        label="Enter News Headline",
        help="You can paste your news headline here"
    ) # Ask user for news headline input

    col1, col2, col3 = st.columns(3) # center the submit button

    with col2:
        submit = st.button(
            label="Evaluate Tone🎭",
        )

    if submit:
        news_topic = topic(query)
        news_sentiment = classification(query)
        news_entity = extract_company(query)

        # Show news entity tag
        if news_entity != "":
            st.button(news_entity, disabled=True, key=f"entity_button")

        # Show news sentiment tag
        if news_sentiment != "":
            if news_sentiment == "bullish":
                news_sentiment = f":green[{news_sentiment}]"
            elif news_sentiment == "bearish":
                news_sentiment = f":red[{news_sentiment}]"
            elif news_sentiment == "neutral":
                news_sentiment = f":white[{news_sentiment}]"
        
            st.button(news_sentiment, disabled=True, key=f"sentiment_button")

        # Show news topic tag
        if news_topic != "":
            news_topic = f":white[{news_topic}]"
            st.button(news_topic, disabled=True, key=f"topic_button")



with tab2:
    # Function to Retrieve news info table from google sheet
    #@st.cache_data
    def load_data(sheets_url):
        csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
        df = pd.read_csv(csv_url)
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        df = df.sort_values(by=["Date"], ascending=False)
        return df

    # Retrieve news info table from google sheet
    df = load_data(st.secrets["public_gsheets_url"])
    df.dropna(inplace=True)

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:
        sent_filter = st.selectbox(
            "Sentiment",
            options=["All", "Bullish", "Neutral", "Bearish"],
            key="sent_filter",
            help="Filter news headline by sentiment"
        )

    if sent_filter != "All":
        sent_filter = sent_filter.lower()
        mask = df["Sentiment"] == sent_filter
        df = df[mask]



    for i in range(len(df)):

        with st.container(border=True):
            news = df.iloc[i]["News"]
            entity = df.iloc[i]["Entity"]
            topic = df.iloc[i]["Topic"]
            sentiment = df.iloc[i]["Sentiment"]
            date = df.iloc[i]["Date"]

            st.write(date)
            st.write("\n"+news)

            entity_col, sent_col, topic_col = st.columns(3)

            if isinstance(entity, str) and entity != "-":
                entities = entity.replace(",", ", ")
                with entity_col:
                    st.button(entities, disabled=True, key=f"entity_key{i}")

            with sent_col:
                if sentiment == "bullish":
                    sentiment = f":green[{sentiment}]"
                elif sentiment == "bearish":
                    sentiment = f":red[{sentiment}]"
                else:
                    sentiment = f":white[{sentiment}]"
            
                st.button(sentiment, disabled=True, key=f"sentiment_key{i}")

            with topic_col:
                topic = f":white[{topic}]"
                st.button(topic, disabled=True, key=f"topic_key{i}")
    
    st.caption("News Source: _Nairametrics_")
