import pyodbc
import os
import csv
#import difflib


path = "C:\\Users\\user\\PycharmProjects\\Cru-Wine\\CRU\\"
os.chdir(path)
winefile = 'EmpireWine-rates-new.csv'
mrf = 'MissingRates.csv'
ratings = []
encoding = 'UTF-8'
lostrates = []

connectionString = ("Driver={SQL Server Native Client 11.0};"
                    "Server=ASUS\SQLEXPRESS;"
                    "Database=WINELOGIC;"
                    "Trusted_Connection=yes;")
cnxn = pyodbc.connect(connectionString)
cursor = cnxn.cursor()


def select_csv_wines(winefile):
    with open(winefile, 'r', encoding='utf8') as f:
        reader = csv.DictReader(f, delimiter = ';')
        for line in reader:
            ratings.append(line)

    return ratings

def select_winebtl_index(rate):
    pic = rate['Picname']
    ye = rate['Year']

    cursor.execute("SELECT ID_WineB FROM Wine_Bottle WHERE Pic_Name = ? AND Year = ?", (pic, ye))
    results = cursor.fetchall()
    id_winebtl = int(results[0][0])

    print(f'ID of bottle of {ye} is {id_winebtl}')

    return id_winebtl


def select_critic_index(rate):
    cn = rate['Critic_S']
    cr = rate['Critic']

    dt = (cr, cn)

    cursor.execute("SELECT ID_Critic FROM Critics WHERE short_name = ?", cn)
    results = cursor.fetchall()

    if len(results) == 0:
        cursor.execute("INSERT INTO Critics (Critic_name, short_name) VALUES (?, ?)", dt)
        cursor.execute("SELECT ID_Critic FROM Critics WHERE short_name = ?", cn)
        resultsA = cursor.fetchall()
        id_critic = int(resultsA[0][0])
        cnxn.commit()

    else:
        id_critic = int(results[0][0])

    print(f'Critic {cr} is {id_critic}')

    return id_critic


def insert_critic_score(rate, id_critic, id_winebtl):
    sc = rate['Score']

    dts = (id_critic, id_winebtl)
    cursor.execute("SELECT Score FROM Ratings WHERE ID_Critic = ? AND ID_WineB = ?", dts)
    scor = cursor.fetchall()

    dtss = (id_critic, id_winebtl, sc)

    if len(scor) == 0:
        cursor.execute("INSERT INTO Ratings (ID_Critic, ID_WineB, Score) VALUES (?, ?, ?)", dtss)
        cursor.execute("SELECT ID_Score FROM Ratings WHERE ID_Critic = ? AND ID_WineB = ? AND Score = ?", dtss)
        resultsA = cursor.fetchall()
        id_score = int(resultsA[0][0])
        cnxn.commit()
    else:
        if scor[0][0] == sc:
            cursor.execute("SELECT ID_Score FROM Ratings WHERE ID_Critic = ? AND ID_WineB = ? AND Score = ?", dtss)
            resultsC = cursor.fetchall()
            id_score = int(resultsC[0][0])
        else:
            cursor.execute("INSERT INTO Ratings (ID_Critic, ID_WineB, Score) VALUES (?, ?, ?)", dtss)
            cursor.execute("SELECT ID_Score FROM Ratings WHERE ID_Critic = ? AND ID_WineB = ? AND Score = ?", dtss)
            resultsB = cursor.fetchall()
            id_score = int(resultsB[0][0])
            print('New rating score for this wine')
            cnxn.commit()

    return id_score


def update_rating_description(rate, id_critic, id_winebtl, id_score):
    rt = rate['Rating']

    cursor.execute("SELECT Description FROM Ratings WHERE ID_Score = ? ", id_score)
    ress = cursor.fetchall()

    if len(ress) == 0 or ress[0][0] == None:
        dta = (rt, id_score)
        cursor.execute("UPDATE Ratings SET Description = ? WHERE ID_Score = ?", dta)
        print(id_score)
        cnxn.commit()
    else:
        print('Rating Description Already In')


if __name__ == '__main__':
    ratings = select_csv_wines(winefile)
    for rate in ratings:
        print(rate['Title'])
        try:
            id_winebtl = select_winebtl_index(rate)
            id_critic = select_critic_index(rate)
            if len(rate['Score']) > 0:
                id_score = insert_critic_score(rate, id_critic, id_winebtl)
            if len(rate['Rating']) > 0:
                update_rating_description(rate, id_critic, id_winebtl, id_score)
        except:
            print('Anything wrong with rating')
            lostrates.append(rate)
            print(len(lostrates))
        if len(lostrates) > 0:
            with open(mrf, 'w', newline='', encoding='utf8') as fl:
                writer = csv.writer(fl, delimiter=';')
                writer.writerow(['Producer', 'Title', 'Year', 'Picname', 'Critic', 'Critic_S', 'Score','Rating'])
                for r in lostrates:
                    writer.writerow(
                        [r['Producer'], r['Title'], r['Year'], r['Picname'], r['Critic'],
                         r['Critic_S'], r['Score'], r['Rating']])

    cnxn.close()

