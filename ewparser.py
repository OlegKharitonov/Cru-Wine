import requests
from bs4 import BeautifulSoup as BS

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44',
    'accept': '*/*'}

ratings = []
wines = []

def get_item_content(item, winecolor):
    req = requests.get(item, headers=HEADERS).text
    soupre = BS(req, 'html.parser')

    title2 = soupre.find('div', class_='col-12').find_next('h1').get_text(strip=True)
    title1 = title2.replace('1.5L', '').replace('3.0L', '').replace("'", '').strip()

    if '20' in title1[-4:]:
        year = title1[-4:].strip()
        title = title1[0:-5].strip()
    elif '19' in title1[-4:]:
        year = title1[-4:].strip()
        title = title1[0:-5].strip()
    else:
        year = '0000'
        title = title1

    price1 = soupre.find('div', class_='clearfix mb-2').find_next('span').get_text(strip=True)
    price = price1.replace('$', '').strip()

    producer = ''
    producer_f = ''
    grapes = ''
    country = ''
    region = ''
    size = ''
    sub = ''

    its = []
    y = soupre.find_all('div', class_='col-12 col-md-6')
    for z in y:
        its.append(z.get_text(strip=True))

    for ee in its:
        if 'Winery' in ee:
            producer_f = ee.split('Winery:')[1].strip()
            producer = producer_f.replace('Winery', '').replace('Château', '').replace('Cellar', '').replace(
                'Bodegas', '').replace( 'Vineyards', '').replace('Wines','').strip()
        if 'Category' in ee:
            grapes = ee.split('Category:')[1].strip()
        if 'Region' in ee:
            land = ee.split('egion:')[1].strip()
            if '»' in land:
                country = land.split('»')[0].strip()
                sub1 = land.split('»')[1].strip()
                region = land.split('»')[1].strip()
                if 'California' in country:
                    country = 'USA'
                    sub = sub1
                    region = 'California'
                elif 'Oregon' in country:
                    country = 'USA'
                    sub = sub1
                    region = 'Oregon'
                elif 'New York' in country:
                    country = 'USA'
                    sub = sub1
                    region = 'New York'
                elif 'Washington' in country:
                    country = 'USA'
                    sub = sub1
                    region = 'Washington'
                elif 'Toscana IGT' in land:
                    country = 'Italy'
                    region = 'Tuscany'
                    sub = 'Toscana IGT'
                elif 'Chianti' in land:
                    country = 'Italy'
                    region = 'Tuscany'
                    sub = 'Chianti'
                elif 'Langhe' in land:
                    country = 'Italy'
                    region = 'Piedmont'
                    sub = 'Langhe'
                elif 'Barolo' in land:
                    country = 'Italy'
                    region = 'Piedmont'
                    sub = 'Barolo'
                elif 'Barbaresco' in land:
                    country = 'Italy'
                    region = 'Piedmont'
                    sub = 'Barbaresco'
                elif 'Montalcino' in land:
                    country = 'Italy'
                    region = 'Tuscany'
                    sub = 'Brunello di Montalcino'
                elif 'Chateauneuf-du-Pape' in land:
                    country = 'France'
                    region = 'Rhône'
                    sub = 'Chateauneuf-du-Pape'
                elif 'Gigondas' in land:
                    country = 'France'
                    region = 'Rhône'
                    sub = 'Gigondas'
                elif 'Cornas' in land:
                    country = 'France'
                    region = 'Rhône'
                    sub = 'Cornas'
                elif 'Cotes du Rhone' in land:
                    country = 'France'
                    region = 'Rhône'
                    sub = 'Cotes du Rhône'
                elif 'Haut-Medoc' in land:
                    country = 'France'
                    region = 'Bordeaux'
                    sub = 'Haut-Medoc'
                elif 'Margaux' in land:
                    country = 'France'
                    region = 'Bordeaux'
                    sub = 'Margaux'
                elif 'Rioja' in land:
                    country = 'Spain'
                    region = 'Castilla y Leon'
                    sub = 'Rioja'
                elif 'Jumilla' in land:
                    country = 'Spain'
                    region = 'Region de Murcia'
                    sub = 'Jumilla'
            else:
                country = land
                if 'California' in land:
                    country = 'USA'
                    region = 'California'
                    sub = 'California'
                elif 'Oregon' in land:
                    country = 'USA'
                    region = 'Oregon'
                    sub = 'Oregon'

        if len(sub) == 0:
            sub = region


        if 'Size' in ee:
            if '1.5' in ee:
                size = '1500'
            elif '3L' in ee:
                size = '3000'
            else:
                size = '750'

    if soupre.find('div', class_='col-12 mb-30'):
        pp = soupre.find('div', class_='col-12 mb-30').get_text(strip=True)
        producer_notes = pp.replace("\'", "'").replace('в?"', '').replace('вЂ“', '-')
    else:
        producer_notes = ''

    if soupre.find('div', class_='mt-2 weight-lite'):
        des = soupre.find('div', class_='mt-2 weight-lite').get_text(strip=True)
        if 'Wine Spectator' or 'Wine Advocate' in des:
            winedes = ''
        else:
            winedes = des
    else:
        winedes = ''


    if soupre.find('div', class_='col-12'):
        try:
            image = soupre.find('div', class_='col-12').find_next('a').get('href')
            name = title1.replace('/', '-').replace('\\', '-').replace('*', '-').replace(',', '').replace('"', '').replace(
                "'", '').replace('â', 'a').replace('ô', 'o').replace('é', 'e').replace('è', 'e')
            picname = name + '.' + image.split('.')[-1][0:3]
            im_file = open(picname, 'wb')
            p = requests.get(image, headers=HEADERS)
            im_file.write(p.content)
            im_file.close()
        except:
            print(f'error with image {item}')
            picname = ''
    else:
        print('No Image')
        picname = ''

    titlename = title.replace(producer, '').strip()

    wines.append({
        'country': country,
        'region': region,
        'subregion': sub,
        'producer': producer,
        'producer_f': producer_f,
        'prod_des': producer_notes,
        'title': titlename,
        'class': '',
        'color': winecolor,
        'grapes': grapes,
        'wine_notes': '',
        'year': year,
        'alcohol': '',
        'maturity': '',
        'description': winedes,
        'pic': picname,
        'size': size,
        'price': price,
        'currency': 'USD',
        'tax': 'exc',
        'store': 'EmpireWine',
        'store_co': 'USA',
        'store_ci': 'ecommerce',
        'date': '2021-04-15'
    })

    return wines


def get_rate_content(item, wines):
    w = wines[-1]
    producer = w['producer']
    title = w['title']
    year = w['year']
    picname = w['pic']

    req = requests.get(item, headers=HEADERS).text
    soupre = BS(req, 'html.parser')

    if soupre.find('div', class_='col-12 mb-3'):
        notes = str(soupre.find('div', class_='col-12 mb-3').get_text)
    else:
        notes = ''

    ots = []

    if len(notes) > 0:
        ots = notes.replace('вЂ™', "'").replace(r"\'", "'").replace('<br/>', ' * ').replace('<bound method '
                            'Tag.get_text of <div class="col-12 mb-3">', '').replace('</div>>', '').replace('amp;',
                            '').split(' *  * ')

    critics = {'Wine & Spirits': 'WAS', 'Wine Advocate': 'WA', 'James Suckling': 'JS', 'Wine Spectator': 'WS',
               'Wilfred Wong': 'WW', 'Wine Enthusiast': 'WE', 'Vinous Media': 'VIN', 'Decanter': 'D',
               'Jeb Dunnuck': 'JD'}

    for art in ots:
        for cr in critics.items():
            if cr[0] in art:
                critic = cr[0].replace('Media', '').strip()
                ratings.append({
                    'producer': producer,
                    'title': title,
                    'year': year,
                    'pic': picname,
                    'critic_name': critic,
                    'critic_sh': cr[1],
                    'score': art.split('*')[0].replace(cr[0], '').strip(),
                    'rating': art
                })
            else:
                pass

    return ratings
