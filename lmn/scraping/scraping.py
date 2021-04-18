import requests
from bs4 import BeautifulSoup

url = 'https://first-avenue.com/shows/?orderby=past_shows'

def scrape_first():
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
    except Exception as e:
        print(e)
    
# selecting elements with <div class="d-flex flex-column h-100 flex-fill">
    seive = soup.select('.h-100')
    print(seive)
    # for item in seive:
    #     print(item)

scrape_first()