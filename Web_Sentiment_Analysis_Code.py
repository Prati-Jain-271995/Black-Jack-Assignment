#!/usr/bin/env python
# coding: utf-8

# In[2]:


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
stemmer = PorterStemmer()


# In[50]:


positive = pd.read_csv('C:\\Users\\HP15\\Downloads\\Positive_Score.csv',index_col=False)
negative = pd.read_csv('C:\\Users\\HP15\\Downloads\\Negative_Score.csv',index_col=False)

positive['Word']= positive['Word'].str.lower()
negative['Word']=negative['Word'].str.lower()


# In[53]:


Urls = pd.read_excel('C:\\Users\\HP15\\Downloads\\Input.xlsx')
Urls = Urls['URL']


# In[54]:


headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
}
page = requests.get(Urls.iloc[1], headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')


# In[55]:


title = soup.title.string


# In[56]:


URL_ID = soup.find_all('p')


# In[57]:


# Word Tokenization
clean_text_1 = []
word_list=[] 
for i in URL_ID:
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    clean = tokenizer.tokenize(i.string)
    clean_text_1.append(clean)
    word_list.append(i.string.split(' '))


# In[58]:


# Sent Tokenization

sent_lis = []

for i in URL_ID:
    sent_lis.append(sent_tokenize(i.string))


# In[59]:


#Calculating number of sentences
total_sent_count = 0

for n in sent_lis:
    for wor in n:
        total_sent_count += 1


# In[60]:


# Converting to lower

clean_text_2=[]

for i in clean_text_1:
    for words in i:
        
        clean_text_2.append(words.lower())
        


# In[61]:


#Text Normalization

clean_text_3 = []
 
#for words in clean_text_2:
    #clean_text_3.append(stemmer.stem(words))
    
for words in clean_text_2:
    
    clean_text_3.append(re.sub('[^a-zA-Z0-9]+','', words))
    


# In[62]:


# Stop-Words Removal

nltk.download('stopwords')
from nltk.corpus import stopwords


# In[63]:


skip_stop_words = lambda x: [w for w in x if w not in stopwords.words('english')]

clean_text_4 = []
clean_text_4 = skip_stop_words(clean_text_3)


# In[64]:


#Word Stemming

clean_text_5 = []

for words in clean_text_4:
    clean_text_5.append(stemmer.stem(words))


# In[65]:


#Lemitization

from nltk.stem.wordnet import WordNetLemmatizer
nltk.download('wordnet')


# In[66]:


wnet = WordNetLemmatizer()


# In[67]:


clean_text_6 = []
for words in clean_text_5:
        clean_text_6.append(wnet.lemmatize(words))


# ## Extracting derived variables

# In[68]:


# Count Positive Words

positive_score_count = lambda x: len([w for w in x if w in list(positive['Word'])])

positive_score=int(positive_score_count(clean_text_6))

positive_score


# In[69]:


# Count Negative Words

negative_score_count = lambda x: len([w for w in x if w in list(negative['Word'])])

negative_score = int(negative_score_count(clean_text_6))

negative_score


# In[70]:


# Calculating Polarity Score

polarity_score= (positive_score-negative_score)/((positive_score+negative_score)+0.000001)

polarity_score


# In[72]:


# Calculating Subjective Score

subjectivity_score= (positive_score + negative_score)/ ((len(clean_text_6)) + 0.000001)

subjectivity_score


# In[73]:


#Calculating total number of words

total_word_count= 0
all_word_list = []

for item in word_list:
    for element in item:
        total_word_count += 1
        all_word_list.append(element)
        


# In[74]:


#Avg Sentence length

average_sentence_length = total_word_count / total_sent_count

average_sentence_length


# In[75]:


# Syllable count per word 

def vowelCounter(listName):
    vowels = 'aeiouAEIOU'
    word_vowel  = []
    TC =[]
    for i in listName:
        for word in i:
            count = 0
            for letter in word:
                if (word[-2:]!='es'and word[-2:]!='ed') and letter in vowels:
                        word_vowel.append(word)
                        count += 1
            TC.append(count)

            

    return TC

total_count_syllable = vowelCounter(word_list)


# In[76]:


# counting complex words - contain more than two syllables

def complex_words(lis):
    count = 0
    
    for i in lis:
        if i>2:
            count += 1
    return count 

# Percentage of complex words
total_count_complex_words = complex_words(total_count_syllable)

percent_of_complex_words = total_count_complex_words/total_word_count


# In[77]:


percent_of_complex_words


# In[78]:


# Fog Index

fog_index = 0.4*(average_sentence_length+percent_of_complex_words)

fog_index


# In[79]:


# Average Number of Words Per Sentence

average_number_of_words_per_sent = total_word_count/total_sent_count

average_number_of_words_per_sent


# In[80]:


# Total count of complex words

total_count_complex_words


# In[81]:


# Word Count

len(clean_text_4)


# In[82]:


# Syllable Count per Word

sum(total_count_syllable)


# In[83]:


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


pronount_count(all_word_list)


# In[84]:


# Calculating total number of characters

count = [len(i) for i in all_word_list]

total_characters = sum(count)


# In[85]:


# Calculating average word length

avg_word_length = total_characters/total_word_count

avg_word_length


# In[ ]:




