import requests
import re
import random
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize

import pandas as pd
import numpy as np

random.seed(10)

# get list of wikipedia pages from list of featured wikipedia pages
articles = requests.get('https://en.wikipedia.org/wiki/Wikipedia:Featured_articles#Culture_and_society')
articles_bs = BeautifulSoup(articles.text, 'lxml')

links = []
 
for link in articles_bs.findAll('a', attrs={'href': re.compile("^/wiki")}):
    links.append(link.get('href'))


# randomly select 500, remove first 35 as they are not links to interesting Wikipedia pages
articles = random.sample(links[35:], 200)
articles


# helper functions for data cleaning
def remove_html_tags(text):
    tags = re.compile(r'<[^>]+>')
    return tags.sub('', text)

def remove_citations(text):
    return re.sub(r'\[[^)]*\]', '', text)

def remove_newline(text):
    return re.sub('\n', '', text)


# function to extract sentences into a list
def list_of_sentences(partial_wikipedia_link):
    html = requests.get('https://en.wikipedia.org/' + partial_wikipedia_link)
    page_bs = BeautifulSoup(html.text, 'lxml')

    selected_data = []

    data = page_bs.find_all(['p'])

    for i in range(len(data)):
        cleaned = remove_html_tags(str(data[i]))
        cleaned = remove_citations(cleaned)
        cleaned = remove_newline(cleaned)
        selected_data.append(cleaned)
    
    while('' in selected_data): 
        selected_data.remove('')
    
    sentence_list = sent_tokenize(''.join(selected_data))
    
    return sentence_list
