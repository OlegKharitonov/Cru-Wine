import csv

def save_csv_ratings(ratings, file1):
    with open(file1, 'a', newline='', encoding='utf8') as fl:
        writer = csv.writer(fl, delimiter=';')
        #writer.writerow(['Producer', 'Title', 'Year', 'Picname', 'Critic', 'Critic_S', 'Score','Rating'])
        for rate in ratings:
            writer.writerow([rate['producer'], rate['title'], rate['year'], rate['pic'], rate['critic_name'],
                             rate['critic_sh'], rate['score'], rate['rating']])