import requests
from bs4 import BeautifulSoup
from lmn.models import Venue, Artist, Note, Show

def scrape_first():
    url = 'https://first-avenue.com/shows/?orderby=past_shows'
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
    except Exception as e:
        print(e)
    
# selecting elements with <div class="d-flex flex-column h-100 flex-fill">
    container_object = soup.find_all(class_="h-100")
    test_data = []
    for html_item in container_object:
        day_bs4_result_set = html_item.select('.day')
        if day_bs4_result_set:
            day = str(day_bs4_result_set[0].text).strip()
            month_bs4_result_set = html_item.select('.month')
            month = str(month_bs4_result_set[0].text).strip()
            year_bs4_result_set = html_item.select('.year')
            year = str(year_bs4_result_set[0].text).strip()
            date = year + ' ' + month + ' ' + day

            venue_name_bs4_result_set = html_item.select('.venue_name')
            venue_name = str(venue_name_bs4_result_set[0].text).strip()
            band_name_bs4_result_set = html_item.select('a')
            band_name = str(band_name_bs4_result_set[0].text).strip()

            try:
                a = Artist(name=band_name)
                a.save()
                
                v = Venue(name=venue_name, city='Minneapolis', state='MN')
                v.save()

                s = Show(show_date=date, artist=band_name, venue=venue_name)
                s.save()
            except Exception as e:
                print(e)
            # print(f'{day} {month} {year}, {venue_name}. {band_name}')
 
if __name__ == "__main__":
    scrape_first()