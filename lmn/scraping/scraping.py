import requests
from bs4 import BeautifulSoup

url = 'https://first-avenue.com/shows/?orderby=past_shows'

def scrape_first():
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        print(soup)    
    except Exception as e:
        print(e)
    


scrape_first()