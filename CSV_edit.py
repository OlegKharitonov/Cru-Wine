from wine_region import region
import csv

editwines = []

def csv_editing(fw):
    with open(fw, newline = '', encoding ='utf8') as csvfile:
        header = next(csvfile)
        reader = csv.reader(csvfile, delimiter = ';')
        for row in reader:
            r = row[2]
            new_c, new_r, new_s = region(r)

            if new_c == '':
                print(f'No search region for {r}')
                new_c = row[0]
                new_r = row[1]
                new_s = row[2]

            row[0] = new_c
            row[1] = new_r
            row[2] = new_s

            editwines.append({
                'country': row[0],
                'region': row[1],
                'subregion': row[2],
                'producer': row[3],
                'producer_f': row[4],
                'prod_des': row[5],
                'title': row[6],
                'class': row[7],
                'color': row[8],
                'grapes': row[9],
                'wine_notes': row[10],
                'year': row[11],
                'alcohol': row[12],
                'maturity': row[13],
                'description': row[14],
                'pic': row[15],
                'size': row[16],
                'price': row[17],
                'currency': row[18],
                'tax': row[19],
                'store': row[20],
                'store_co': row[21],
                'store_ci': row[22],
                'date': row[23]
            })

    return editwines
