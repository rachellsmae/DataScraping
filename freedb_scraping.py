import tarfile
import re
import requests
import json
import os
import shutil
import pickle
import sys

# basic
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
import pickle
import unidecode
import unicodedata as ud


# ran code on multiple clusters because the folder was very big
inputid = int(sys.argv[2])
start = inputid*300000
end = (inputid+1) * 300000
print(start, end)


# import freedb data
tar = tarfile.open('freedb-update-20190215-20190301.tar.bz2', 'r:bz2') # this is the updated info, the complete file is larger
tar_members = tar.getmembers()
length = len(tar_members)
print(length)

if os.path.exists('data'):
    shutil.rmtree('data')
else:
    print("no file deleted. Data does not exist")

tar.extractall('data'+str(inputid), members=tar_members[start:min(end, length)])


# function to extract artist name
def extract_artist(elements):
    #print(elements)
    interested_element = elements[0]
    if '\\' in interested_element:
        interested_element = interested_element.replace('\\', '')
    if '\t' in interested_element:
        interested_element = interested_element.replace('\t', '')
    return interested_element.split(' /')[0]


# functions to check if string only contains roman letters
latin_letters= {}

def is_latin(uchr):
    try: return latin_letters[uchr]
    except KeyError:
        return latin_letters.setdefault(uchr, 'LATIN' in ud.name(uchr))

def is_roman_chars(unistr):
    return all(is_latin(uchr)
        for uchr in unistr
        if uchr.isalpha())


# function to return empty string if nan, first elem otherwise
def return_empty(list_of_elem):
    if len(list_of_elem) == 0:
        return ''
    else:
        return list_of_elem[0]


# function to find info on each data file
def find_info(string):
    artist = ''
    year = ''
    genre = ''
    tracks = ''
    
    if string != "":
        artist = extract_artist(re.findall('(?<=DTITLE=)[A-Za-z0-9 \t\\\\N!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+', string))
        year = return_empty(re.findall('(?<=DYEAR=)[0-9]+', string))
        genre = return_empty(re.findall('(?<=DGENRE=)[A-Za-z0-9]+', string))
        tracks = re.findall('(?<=TTITLE[0-9]=)[A-Za-z0-9 !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+', string)

    return artist, year, genre, tracks


# running
sub_files = os.listdir('data'+str(inputid))[0]
files = os.listdir('data'+str(inputid)+'/' + sub_files)
dictionary = {}

for fi in files:
    file_name = 'data'+str(inputid)+'/' + sub_files + '/' + fi
    
    try:
        with open(file_name, 'rb') as f:
            string = unidecode.unidecode(f.read().decode('utf-8'))#.split('\n')
    
    except UnicodeDecodeError:
        with open(file_name, 'rb') as f:
            string = unidecode.unidecode(f.read().decode('latin-1'))#.split('\n')

    if is_roman_chars(string):
        file_data = find_info(string)
        
        # if not 'various artists'
        if 'various' not in file_data[0].lower():
            tuples = [(file_data[0], i) for i in file_data[3]]
            for j in tuples:
                dictionary[j] = (file_data[1], file_data[2])

        # if various artists
        else:
            tuples = [(i.split(' / ')[0], i.split(' / ')[1]) for i in file_data[3] if ' / ' in i]
            tuples = [(i.split(' - ')[0], i.split(' - ')[1]) for i in file_data[3] if ' - ' in i]
            for j in tuples:
                dictionary[j] = (file_data[1], file_data[2])
    else:
        continue
        
if os.path.exists('data'+str(inputid)+'/' + sub_files):
    shutil.rmtree('data'+str(inputid)+'/' + sub_files)
else:
    print('The file does not exist for deletion')

with open('dictionary' + str(inputid) + '.pickle', 'wb') as handle:
    pickle.dump(dictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)

