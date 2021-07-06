import streamlit as  st
import plotly.express as px
import numpy as np
import pandas as pd

df = pd.read_csv(r'C:\Users\j.elachkar.ENSRVG\Desktop\Tweets.csv')
print(df)
df['tweet_created'] = pd.to_datetime(df['tweet_created'])
st.title("Sentiment Analysis of Tweets about US Airlines ")
st.sidebar.subheader("this application is a streamlit application to analyse the sentiment of tweets")
st.sidebar.markdown("Show Random tweet")
radio = st.sidebar.radio("select the sentiment",['neutral','positive','negative'],key='1')
st.sidebar.markdown(df.query('airline_sentiment==@radio')['text'].sample(n=1).values)

st.sidebar.subheader("Number of tweets by sentiment")
select = st.sidebar.selectbox("Visualization type",["Histogram","Pie Chart"])
data = df['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'sentiment':data.index,'Tweets':data.values})

if not st.sidebar.checkbox("Hide",True):
    if select == "Histogram":
        fig = px.bar(sentiment_count,x='sentiment',y='Tweets',height=500)
        st.plotly_chart(fig)
    else:
        fig1=px.pie(sentiment_count,names='sentiment',values='Tweets')
        st.plotly_chart(fig1)

st.sidebar.subheader("when and where are users tweeting from")
hour = st.sidebar.slider("Hour",min_value=1,max_value=23)
modified_data = df[df['tweet_created'].dt.hour==hour]

if not st.sidebar.checkbox("close",True,key='5'):
    st.markdown("### Tweets Locations based on time of day")
    st.markdown("%i tweets between %i:00 and %i:00" % (len(modified_data),hour,(hour+1)%24))
    st.map(modified_data)

if st.sidebar.checkbox("show raw data",False): # we are  not going to show the raw data by default
    st.write(df)

st.sidebar.subheader("Breakdown airline tweets by sentiment")
choice = st.sidebar.multiselect("Pick airlines",['American','Delta','Southwest','United','Us Airways','Virgin America'])

if len(choice) >0:
    choice_data = df[df.airline.isin(choice)]
    fig_choice = px.histogram(choice_data,x='airline',y='airline_sentiment',histfunc='count',color='airline_sentiment',
                              facet_col='airline_sentiment',labels={'airline_sentiment':'tweets'},height=600,width=800)
    st.plotly_chart(fig_choice)


