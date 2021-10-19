

BWS = ({'site':'EmpireWine', 'url':'empirewine.com', 'store_co' :
       'USA', 'store_ci': 'ecommerce', 'currency': 'USD', 'tax': 'exc'}, {'site':'Bodeboca', 'url': 'bodeboca.com',
       'store_co' : 'Spain', 'store_ci': 'ecommerce', 'currency': 'EUR', 'tax': 'inc'}, {'site': 'CampoluzEnoteca',
       'url': 'campoluzenoteca.com', 'store_co' : 'Spain', 'store_ci': 'ecommerce', 'currency': 'EUR', 'tax': 'inc'})

pgs = ('https://www.campoluzenoteca.com/vino-tinto/s/7496#s[14][]:&s[13][]:1992&sid:1&h:leftColumn&id_seo:7496&p:3',
       'https://www.campoluzenoteca.com/vino-blanco/s/7497#s[14][]:&s[13][]:1987&sid:1&h:leftColumn&id_seo:7497&p:3',
       'https://www.campoluzenoteca.com/vino-rosado/s/7495#s[14][]:&s[13][]:1991&sid:1&h:leftColumn&id_seo:7495&p:2',
       'https://www.campoluzenoteca.com/vino-espumoso/s/7498#s[14][]:&s[13][]:1989&sid:1&h:leftColumn&id_seo:7498&p:3'
       'https://www.campoluzenoteca.com/vino-dulce/s/7499#s[14][]:&s[13][]:1988&sid:1&h:leftColumn&id_seo:7499&p:2')

for Store in BWS:
       site = Store['site']

       print(site)
