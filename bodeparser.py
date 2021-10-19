import requests
from bs4 import BeautifulSoup as BS

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44',
    'accept': '*/*'}

ratings = []
wines = []

def get_item_bcontent(item, winecolor, site):
    req = requests.get(item, headers=HEADERS).text
    soupre = BS(req, 'html.parser')

    price1 = soupre.find('div', class_='pricebox-part1').get_text(strip=True)
    price = price1.split('€')[0].replace(',', '.').strip()
    if '150 cl' in price1:
        size = '1500'
    elif '37,5' in price1:
        size = '375'
    elif '300' in price1:
        size = '3000'
    else:
        size = '750'

    pla = str(soupre.find('div', class_='field-item odd').find_next('span'))

    if 'country-317' in pla:
        country = 'Spain'
    elif 'country-318' in pla:
        country = 'France'
    elif 'country-319' in pla:
        country = 'Portugal'
    elif 'country-351' in pla:
        country = 'Italy'
    elif 'country-334' in pla:
        country = 'Argentina'
    elif 'country-335' in pla:
        country = 'Australia'
    elif 'country-336' in pla:
        country = 'New Zealand'
    elif 'country-433' in pla:
        country = 'Germany'
    elif 'country-501' in pla:
        country = 'South Africa'
    elif 'country-504' in pla:
        country = 'Chile'
    else:
        country = ''

    nts = []
    infos = soupre.find('div', class_='info three-column-wrapper product-details')
    ins =  infos.find_all('div', class_='field')
    for i in ins:
        nts.append(i.get_text(strip=True))

    producer = ''
    producer_f = ''
    titlename = ''
    grapes = ''
    region = ''
    sub = ''
    year = ''
    alc = ''
    grapes = ''
    description = ''

    for el in nts:
        if 'La bodega' in el:
            producer_f = el.replace('La bodega:', '').strip()
            producer = producer_f.replace('Bodegas y viñedos', '').replace('Adega', '').replace('Bodegas', '') .replace\
                        ('Viñedos', '').replace('Domaine', ''). replace('Maison', ''). replace(
                        'Wines', '').replace('Chateau', '').replace('Château', '').replace('y viñedos', '').replace(
                        'Weingut','').replace('Bodega', '').replace('Estate', '').replace('Celler del', '').replace(
                        'Vinos', '').replace('Cellers', '').strip()
        if 'Marca' in el:
            title1 = el.replace('Marca:', '').strip()
            titlename = title1.replace(producer_f, '').replace(producer, '').replace('Magnum', '').strip()
            if titlename == 'Chateau':
                titlename = producer
            elif titlename == '':
                titlename = producer
        if 'D.O.' in el:
            region = el.replace('D.O.:', '')
        if 'Añada' in el:
            year = el.replace('Añada:', '').strip()
        if 'Grado' in el:
            alc = el.replace('Grado:', '').replace('vol.', '').replace('Vol.', '').strip()
        if 'Variedad' in el:
            grapes = el.replace('Variedad:', '').strip()
        if 'Producción' in el:
            production = el.replace('Producción:', '').replace('.', '').strip()
            description = production
        if 'Subzona' in el:
            sub = el.replace('Subzona:', '').strip()
        else:
            sub = region

        if '1er Cru' in titlename:
            classif = '1er Cru'
        elif 'Grand Cru' in titlename:
            classif = 'Grand Cru'
        else:
            classif = ''


    if soupre.find('div', id='mainimage'):
        try:
            image = soupre.find('div', id='mainimage').find_next('a').get('href')
            name = title1.replace('/', '-').replace('\\', '-').replace('*', '-').replace(',', '').replace('"', '').replace(
                "'", '').replace('â', 'a').replace('ô', 'o').replace('é', 'e').replace('è', 'e') + ' ' + year.strip()
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


    wines.append({
        'country': country,
        'region': region,
        'subregion': sub,
        'producer': producer,
        'producer_f': producer_f,
        'prod_des': '',
        'title': titlename,
        'class': classif,
        'color': winecolor,
        'grapes': grapes,
        'wine_notes': '',
        'year': year,
        'alcohol': alc,
        'maturity': '',
        'description': description,
        'pic': picname,
        'size': size,
        'price': price,
        'currency': 'EUR',
        'tax': 'inc',
        'store': site,
        'store_co': 'Spain',
        'store_ci': 'Madrid',
        'date': '2021-04-20'
    })

    return wines


def get_rate_bcontent(item, wines):
    w = wines[-1]
    producer = w['producer']
    title = w['title']
    year = w['year']
    picname = w['pic']

    req = requests.get(item, headers=HEADERS).text
    soupre = BS(req, 'html.parser')

    if soupre.find('div', class_='icons mobile-padding'):
        rts = soupre.find('div', class_='icons mobile-padding')
        notes1 = rts.find_all('div', class_='item')
        notes = []
        for n in notes1:
            nnew = n.get_text(strip=True)
            notes.append(nnew.replace('Parker', " Wine Advocate").replace("Suckling", " James Suckling").replace(
                'Peñín',' Peñín').replace('Decanter', ' Decanter').replace('WS', ' Wine Spectator').replace
                ('Revue du Vin de France', ' Revue du Vin de France').replace('WE', ' Wine Enthusiast').replace
                ('Tim Atkin', ' Tim Atkin').replace('Dunnuck', ' Jeb Dunnuck'))
    else:
        notes = ['']

    if soupre.find('div', class_='info opinion opinionrow expert-reviews'):
        rtss = soupre.find('div', class_='info opinion opinionrow expert-reviews')
        tes1 = rtss.find_all('div', class_='field')
        notesfull = []
        for n in tes1:
            notesfull.append(n.get_text(strip=True))
    else:
        notesfull = ['']

    critics = {'Wine & Spirits': 'WAS', 'Wine Advocate': 'WA', 'James Suckling': 'JS', 'Wine Spectator': 'WS',
               'Wilfred Wong': 'WW', 'Wine Enthusiast': 'WE', 'Vinous Media': 'VIN', 'Decanter': 'D',
               'Jeb Dunnuck': 'JD', 'Peñín': 'PEN', 'Revue du Vin de France': 'RVF', 'Tim Atkin': 'TA'}

    nots = notes + notesfull

    for cr in critics.items():
        rt = []
        critic = cr[0].strip()
        for nt in nots:
            if cr[0] in nt:
                rt.append(nt)
        if len(rt) == 2:
            score = rt[0].split(' ')[0].strip()
            des = rt[-1]
            ratings.append({
                'producer': producer,
                'title': title,
                'year': year,
                'pic': picname,
                'critic_name': critic,
                'critic_sh': cr[1],
                'score': score,
                'rating': des
            })
        elif len(rt) == 1:
            score = rt[0].split(' ')[0].strip()
            des = ''
            ratings.append({
                'producer': producer,
                'title': title,
                'year': year,
                'pic': picname,
                'critic_name': critic,
                'critic_sh': cr[1],
                'score': score,
                'rating': des
            })
        else:
            pass

    return ratings
