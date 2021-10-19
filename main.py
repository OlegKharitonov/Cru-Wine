import os
from winecolor import wine_color
from pagination1 import pagination
from get_pages import mix_pages
from get_items import get_items
from newwines import select_new_wines
from ewparser import get_item_content
from ewparser import get_rate_content
from bodeparser import get_item_bcontent
from bodeparser import get_rate_bcontent
from savewines import save_csv_wines
from saveratings import save_csv_ratings
from CSV_edit import csv_editing
from csvplus import csvfile_plus_csvfile


BWS = ({'site':'EmpireWine', 'url':'empirewine.com', 'store_co' : 'USA', 'store_ci': 'ecommerce', 'currency':
       'USD', 'tax': 'exc'}, {'site':'Bodeboca', 'url': 'bodeboca.com',
       'store_co' : 'Spain', 'store_ci': 'ecommerce', 'currency': 'EUR', 'tax': 'inc'}, {'site': 'CampoluzEnoteca',
       'url': 'campoluzenoteca.com', 'store_co' : 'Spain', 'store_ci': 'ecommerce', 'currency': 'EUR', 'tax': 'inc'})

pgs = ('https://www.empirewine.com/search/?q=pre%3Awine_red&page=1',
       'https://www.empirewine.com/search/?q=pre%3Awine_white&page=1',
       'https://www.empirewine.com/search/?q=pre%3Awine_sparkling&page=1',
       'https://www.empirewine.com/search/?q=pre%3Awine_pink&page=1',
       'https://www.bodeboca.com/vino/tinto?page=2&sort=rating-desc&wine_type=372',
       'https://www.bodeboca.com/vino/blanco?page=2&sort=rating-desc&wine_type=373',
       'https://www.bodeboca.com/vino/rosado?page=2&sort=rating-desc&wine_type=374',
       'https://www.campoluzenoteca.com/vino-tinto/s/7496#s[14][]:&s[13][]:1992&sid:1&h:leftColumn&id_seo:7496&p:3',
       'https://www.campoluzenoteca.com/vino-blanco/s/7497#s[14][]:&s[13][]:1987&sid:1&h:leftColumn&id_seo:7497&p:3',
       'https://www.campoluzenoteca.com/vino-rosado/s/7495#s[14][]:&s[13][]:1991&sid:1&h:leftColumn&id_seo:7495&p:2',
       'https://www.campoluzenoteca.com/vino-espumoso/s/7498#s[14][]:&s[13][]:1989&sid:1&h:leftColumn&id_seo:7498&p:3'
       'https://www.campoluzenoteca.com/vino-dulce/s/7499#s[14][]:&s[13][]:1988&sid:1&h:leftColumn&id_seo:7499&p:2')


items = []
winepages = []
nwines = []
ratings = []
wines = []
mpages = []

if __name__ == '__main__':
    for Store in BWS:
        site = Store['site']
        url = Store['url']
        st_co = Store['store_co']
        st_ci = Store['store_ci']
        cur = Store['currency']
        tax = Store['tax']

        pth = 'E:/WINE-Project/' + site + '/'
        if not os.path.exists(pth):
            os.makedirs(pth)
        os.chdir(pth)

        wf = site + 'Wines.txt'
        wfn = site + 'Wines-New.txt'

        if not os.path.exists(pth + wf):
            mfile = open(wf, 'w')
            mfile.close()
        else:
            pass

        if not os.path.exists(pth + wfn):
            mfile = open(wfn, 'w')
            mfile.close()
        else:
            pass

        fw = site + '-wines.csv'
        fwn = site + '-wines-new.csv'
        fwe = site + '-wines-editing.csv'
        fr = site + '-rates.csv'
        frn = site + '-rates-new.csv'
        fre = site + '-rates-editing.csv'

        for p in pgs[7:8]:
            if url in p:
                winepages.append(p)
        print(winepages)
        for page in winepages:
            winecolor = wine_color(page)
            print(winecolor)
            max_page = pagination(page)
            print(f'{max_page} pages in {winecolor} wines for {url}')
            mpages = mix_pages(page, max_page)
            print(mpages)
        for pg in mpages:
            items = get_items(pg)
            print(len(items))
        nwines = select_new_wines(wf, wfn, items, site)
        print(len(nwines))
        for item in nwines:
            if 'bodeboca' in item:
                try:
                    wines = get_item_bcontent(item, winecolor,site)
                    ratings = get_rate_bcontent(item, wines)
                except:
                    print(f'Error with item - {item}')
            print(len(wines))
        print(len(ratings))
        save_csv_wines(wines, fw)
        save_csv_ratings(ratings, fr)
        os.remove(wfn)
        #editwines = csv_editing(fw)
        #fw = fwe
        #wines = editwines
        #save_csv_wines(wines, fw)

    #     csvfile_plus_csvfile