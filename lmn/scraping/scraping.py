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
    container_object = soup.select('.h-100')
    for html_item in container_object:
        day = html_item.select('.day').text
        print(day)
    # print(artist)
    # for item in seive:
    #     artist = item.find('a')['href'] 
    #     day = item.find('.day')
    #     month = item.find('.month')
    #     year = item.find('.year')
    #     venue_name = item.find('.venue_name')
    #     print(f'{artist} {day} {month} {year} {venue_name}')
# a href is band title
#div class="month"> Apr
#div class="day">3
#div class="year">2021
#div class="venue_name">Livestream
scrape_first()