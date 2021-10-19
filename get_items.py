import requests
from bs4 import BeautifulSoup as BS

items = []

def get_items(pg):
    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44',
        'accept': '*/*'}

    if 'empirewine.com' in pg:
        r = requests.get(pg, headers=HEADERS)
        html = BS(r.content, 'html.parser')
        for el in html.find_all('h2', class_="product-title"):
            items.append(el.find('a').get('href'))
    elif 'bodeboca' in pg:
        r = requests.get(pg, headers=HEADERS)
        html = BS(r.content, 'html.parser')
        for el in html.find_all('div', class_="wineblock-inner"):
            items.append('https://www.bodeboca.com' + el.find('a').get('href'))
    elif 'campoluzenoteca.com' in pg:
        r = requests.get(pg, headers=HEADERS)
        html = BS(r.content, 'html.parser')
        for el in html.find_all('h5', itemprop="name"):
            items.append(el.find('a').get('href'))
    else:
        print('error')


    return items

