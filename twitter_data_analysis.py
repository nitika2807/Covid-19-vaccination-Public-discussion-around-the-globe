# -*- coding: utf-8 -*-
"""Copy of Copy of Nitika Twitter new.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10WxpcyehFQqtIjTC83rMSveXbFqbREOD
"""

#importing all the necessary libraries
import os
import pandas as pd
import tweepy as tw
from textblob import TextBlob
from wordcloud import WordCloud
import numpy as np
import re
import matplotlib.pyplot as plt

#getting the necessary keys for connection to the API
consumer_key= 'SubfIHv5YO8pbJm7QlvFEv1xT'
consumer_secret= 'FeIayF0uobMxMdsPzlysGjtd9xfv3VeVyK2p7FtxwwBQUfhqT0'
access_token= '1371713821170049029-nGFzP2Qt9aOqxawnrpW2KurzBDZ2Zg'
access_token_secret= '2GLGLo06bZEvz4cXwCb0ggKUJlKjTPD7DlR9ftpwFFDVP'

#authentication object creation
auth = tw.OAuthHandler(consumer_key, consumer_secret)

#access token setup with my own access keys
auth.set_access_token(access_token, access_token_secret)

#API object creation 
api = tw.API(auth, wait_on_rate_limit = True)

#search_term = "Covid-19 vaccination"
#tweet_amount = 10
#posts = tw.Cursor(api.search, q=search_term, lang = "en", tweet_mode = "extended").items(tweet_amount)

#print("show recent 5 tweets: \n")
i = 1
#for tweet in posts:
 # print(str(i) + ') '+ tweet.full_text+ '\n')
 # i = i+1

#create a new dataframe
search_term = "Covid-19 vaccination, Pfizer, Covid Vaccine Dose"
fil_search = search_term + " -filter:retweets"
tweet_amount = 500

posts = tw.Cursor(api.search, q=fil_search, lang = "en", tweet_mode = "extended").items(tweet_amount)

df = pd.DataFrame([tweet.full_text for tweet in posts], columns = ['message'])
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
df.head(tweet_amount)

def finalTxt(text):
  text = re.sub(r'@[A-Za-z0-9]+', '', text) #removing @mentions and unwanted charaters after that
  text = re.sub(r'#', '', text)       #removing hashtags
  text = re.sub(r'https?:\/\/\S+', '', text)     #removing hyperlinks
  text = re.sub(r'[^\w\s]', '', text)      # removing punctuation 

  return text

df['message'] = df['message'].apply(finalTxt)

df

#removal of short words (all the words of length more than 3 are removed using lambda function)
df['message'] = df['message'].apply(lambda x: " ".join([w for w in x.split() if len(w) > 3])) 
df

#tokenization (consideration of individual words as tokens)
tokenized_tweet = df['message'].apply(lambda x: x.split())
tokenized_tweet

#stemming (for putting the words of the same meaning in a single category)
#from nltk.stem.porter import PorterStemmer
#stemmer=PorterStemmer()

#tokenized_tweet = tokenized_tweet.apply(lambda sentence: [stemmer.stem(word) for word in sentence])
#tokenized_tweet

from nltk.corpus import stopwords
import nltk
nltk.download("stopwords")
stop_words = stopwords.words('english')
tokens_without_sw = [w for w in tokenized_tweet if (w not in stop_words)]
tokens_without_sw
#print (stop_words)

#display all tokenized words in a single sentence
for i in range(len(tokens_without_sw)):
  tokens_without_sw[i]= " ".join(tokens_without_sw[i])

df['message']= tokens_without_sw
df

#data vizualization- Vizualization of the frequent words.
#! pip install wordcloud

all_words = " ".join([sentence for sentence in df['message']])

wordcloud = WordCloud(width=800, height=500,random_state=42, max_font_size=100).generate(all_words)

#plot
plt.figure(figsize=(15,8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

#function to get subjectivity
def getSubjectivity(text):
  return TextBlob(text).sentiment.subjectivity

#create a function to get polarity
def getPolarity(text):
  return TextBlob(text).sentiment.polarity

#create two new columns
df['Subjectivity']=df['message'].apply(getSubjectivity)
df['Polarity']=df['message'].apply(getPolarity)

#Show the new dataframe with new columns
df

#function building for the computation of the positive, negative and neutral analysis
def getAnalysis(score):
  if score < 0:
    return 'Negative'
  elif score == 0:
    return 'Neutral'
  else:
    return 'Positive'

df['Analysis']= df['Polarity'].apply(getAnalysis)

df

#print all positive tweets
j=1 
sortedDF= df.sort_values(by=['Polarity'])
for i in range(0, sortedDF.shape[0]):
  if (sortedDF['Analysis'][i] == 'Positive'):
    print(str(j)+ ') '+ sortedDF['message'][i])
    print()
    j= j+1

#print negative tweets
j=1 
sortedDF= df.sort_values(by=['Polarity'], ascending = 'False')
for i in range(0, sortedDF.shape[0]):
  if (sortedDF['Analysis'][i] == 'Negative'):
    print(str(j)+ ') '+ sortedDF['message'][i])
    print()
    j= j+1

#calculate the percentage of positive tweets
pmessage=df[df.Analysis == 'Positive']
pmessage=pmessage['message']
round( (pmessage.shape[0] / df.shape[0]) *100, 1)  #dividing the total number of positive tweets by total number of data in the dataframe

#calculate the percentage of positive tweets
nmessage=df[df.Analysis == 'Negative']
nmessage=nmessage['message']
round( (nmessage.shape[0] / df.shape[0]) *100, 1)  #dividing the total number of positive tweets by total number of data in the dataframe

#Show the count by plotting

#plot and eventually visualize the data
plt.figure(figsize=(10,8))
for i in range(0, df.shape[0]):
  plt.scatter(df['Polarity'][i], df['Subjectivity'][i], color='Green')

plt.title('Sentiment Analysis of Twitter extracted dataset')
plt.xlabel('Polarity')
plt.ylabel('Subjectivity')
plt.show()

#wordcloud of positive tweets
all_words = " ".join([sentence for sentence in df['message'][df['Analysis'] == 'Positive']])

wordcloud = WordCloud(width=800, height=500,random_state=42, max_font_size=100).generate(all_words)

#plot
plt.figure(figsize=(15,8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

#wordcloud of positive tweets
all_words = " ".join([sentence for sentence in df['message'][df['Analysis'] == 'Negative']])

wordcloud = WordCloud(width=800, height=500,random_state=42, max_font_size=100).generate(all_words)

#plot
plt.figure(figsize=(15,8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
