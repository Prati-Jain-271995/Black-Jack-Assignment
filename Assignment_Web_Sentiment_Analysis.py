#!/usr/bin/env python
# coding: utf-8

##Web Sentiment Analysis

import pandas as pd
import requests
import nltk
from nltk.tokenize import  word_tokenize
from nltk.tokenize import  sent_tokenize
nltk.download('punkt')
from nltk.stem.porter import *
from nltk.stem import LancasterStemmer
import re
from bs4 import BeautifulSoup
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
nltk.download('wordnet')
stemmer = PorterStemmer()


positive = pd.read_csv('C:\\Users\\HP15\\Downloads\\Positive_Score.csv',index_col=False)
negative = pd.read_csv('C:\\Users\\HP15\\Downloads\\Negative_Score.csv',index_col=False)

positive['Word']= positive['Word'].str.lower()
negative['Word']=negative['Word'].str.lower()



Urls = pd.read_excel('C:\\Users\\HP15\\Downloads\\Input.xlsx')
Urls = Urls['URL']


headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
}
page = requests.get(Urls.iloc[168], headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')

URL = soup.find_all('p')

listToStr = ' '.join([str(elem) for elem in URL])

URL_ID = BeautifulSoup(listToStr,'lxml').get_text()



# Word Tokenization

clean_text_1 = []

tokenizer = nltk.RegexpTokenizer(r"\w+")
clean_text_1 = tokenizer.tokenize(URL_ID)



# Sent Tokenization

sent_lis = sent_tokenize(URL_ID)
 
    

#Calculating number of sentences

total_sent_count = 0

for n in sent_lis:
        total_sent_count += 1
        

        
# Converting to lower

clean_text_2=[]

for i in clean_text_1:
        
        clean_text_2.append(i.lower())


        
#Text Normalization

clean_text_3 = []
    
for words in clean_text_2:
    
    clean_text_3.append(re.sub('[^a-zA-Z0-9]+','', words))


    
# Stop-Words Removal

skip_stop_words = lambda x: [w for w in x if w not in stopwords.words('english')]

clean_text_4 = []
clean_text_4 = skip_stop_words(clean_text_3)



#Word Stemming

clean_text_5 = []

for words in clean_text_4:
    clean_text_5.append(stemmer.stem(words))
    


# Lemitization

wnet = WordNetLemmatizer()

clean_text_6 = []
for words in clean_text_5:
        clean_text_6.append(wnet.lemmatize(words))


# Extracting derived variables

# Count Positive Words

positive_score_count = lambda x: len([w for w in x if w in list(positive['Word'])])

positive_score=int(positive_score_count(clean_text_6))

positive_score


# Count Negative Words

negative_score_count = lambda x: len([w for w in x if w in list(negative['Word'])])

negative_score = int(negative_score_count(clean_text_6))

negative_score


# Calculating Polarity Score

polarity_score= (positive_score-negative_score)/((positive_score+negative_score)+0.000001)

polarity_score


# Calculating Subjective Score

subjectivity_score= (positive_score + negative_score)/ ((len(clean_text_6)) + 0.000001)

subjectivity_score


#Calculating total number of words

total_word_count= 0
all_word_list = []

for item in clean_text_1:
        total_word_count += 1
        all_word_list.append(item)


#Avg Sentence length

average_sentence_length = total_word_count / total_sent_count

average_sentence_length



# Getting Syllable 

def vowelCounter(listName):

    lis = []
    vowels = 'aeiouAEIOU'
    for wor in listName:
        count=0
        for ch in wor:
            if ch in vowels and (wor[-2:]!='es' and wor[-2:]!='ed'):
                count += 1
        lis.append(count)
    return lis

total_num_vowel_per_word=vowelCounter(all_word_list)


# counting percent of complex words - contain more than two syllables

def complex_words(lis):
    count = 0
    
    for i in lis:
        if i>2:
            count += 1
    return count 


# Percentage of complex words

total_count_complex_words = complex_words(total_num_vowel_per_word)

percent_of_complex_words = total_count_complex_words/total_word_count

percent_of_complex_words


# Fog Index

fog_index = 0.4*(average_sentence_length+percent_of_complex_words)

fog_index


# Average Number of Words Per Sentence

average_number_of_words_per_sent = total_word_count/total_sent_count

average_number_of_words_per_sent


# Total count of complex words

total_count_complex_words


# Word Count

total_word_count_after_cleaning = len(clean_text_4)

total_word_count_after_cleaning


# Syllable Count per Word

total_count_syllable_per_word = sum(total_num_vowel_per_word)/total_word_count

total_count_syllable_per_word


# Counting Pronouns

pronoun_list = ['i','we','ours','my','us']

def pronount_count(word_list):
    
    total_pronoun_count=0
    pronoun_word_lis = []
    
    for word in word_list:
        if word in pronoun_list:
            total_pronoun_count += 1
            pronoun_word_lis.append(word)
            
        
    return total_pronoun_count,pronoun_word_lis


total_pronoun_count,pronoun_word_list = pronount_count(all_word_list)

total_pronoun_count,pronoun_word_list


# Calculating total number of characters

count = [len(i) for i in all_word_list]

total_characters = sum(count)


# Calculating average word length

avg_word_length = total_characters/total_word_count

avg_word_length

