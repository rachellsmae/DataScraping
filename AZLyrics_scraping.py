import requests
from bs4 import BeautifulSoup

# function to return index of second longest element
def second_longest(listi):
    new_list = listi.copy()
    new_list.remove(max(new_list))
    return listi.index(max(new_list))

# function to get lyrics
def get_lyrics(song):
    url = requests.get('https://www.azlyrics.com/lyrics/' + song + '.html')
    soup = BeautifulSoup(url.text, 'html.parser')
    
    # get list of html text
    elem = soup.get_text().split('\r')

    # get length of elements in elem
    length = []
    for i in elem:
        length.append(len(i.split()))
        
       
    # lyrics are usually the longest element in the list
    lyrics = elem[length.index(max(length))]
    
    # but it could also be the description in the bottom. in that case, lyrics are the second longest.
    if 'Submit Corrections' in lyrics:
        lyrics = elem[second_longest(length)]
        
    return lyrics

# format of url is: https://www.azlyrics.com/lyrics/taylorswift/me.html
song_list = [] # insert list of songs: song is formatted as artist/title
scraped_lyrics = []

for song in song_list:
    scraped_lyrics.append(get_lyrics(song))
