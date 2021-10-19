import csv

def save_csv_wines(wines, file):
    with open(file, 'a', newline='', encoding='utf8') as fl:
        writer = csv.writer(fl, delimiter=';')
        # writer.writerow(['Country', 'Region', 'Subregion', 'Producer', 'Producer_Full', 'Producer_Notes', 'Title',
        #                  'Classification', 'Color', 'Grapes', 'Wine_Notes', 'Year', 'Alcohol', 'Maturity',
        #                  'Description', 'Pic_Name', 'Size', 'Price', 'Currency', 'Tax', 'Store','Store_Co', 'Store_Ci', 'Date'])
        for w in wines:
            writer.writerow([w['country'], w['region'], w['subregion'], w['producer'],
                             w['producer_f'], w['prod_des'], w['title'], w['class'], w['color'],
                             w['grapes'], w['wine_notes'], w['year'], w['alcohol'], w['maturity'],
                             w['description'], w['pic'], w['size'], w['price'], w['currency'],
                             w['tax'], w['store'], w['store_co'], w['store_ci'], w['date']])

