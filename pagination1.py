import requests
from bs4 import BeautifulSoup as BS

def pagination(page):
    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44',
        'accept': '*/*'}
    r = requests.get(page, headers=HEADERS)
    html = BS(r.content, 'html.parser')

    if 'empirewine.com' in page:
        sts = html.find_all('li', class_="page-item")
        pgs = []
        for el in sts:
            pg = str(el.find('a', class_='page-link').get_text(strip=True))
            if pg.isdigit():
                pgs.append(int(pg))
        max_page = max(pgs)

    elif 'bodeboca' in page:

        sts = str(html.find('li', class_="pager__item pager__item--last").find_next('a'))
        max_page = int(sts.split('"')[1])

    elif 'campoluzenoteca.com' in page:
        sts = html.find('ul', class_='pagination clearfix li_fl')
        stss = sts.find_all('li')
        for l in stss[-2]:
            max_page = l.get_text(strip=True)

    else:
        max_page = 1

    return max_page

