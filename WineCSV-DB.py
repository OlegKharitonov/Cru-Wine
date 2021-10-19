import pyodbc
import os
import csv
import difflib


path = "C:\\Users\\user\\PycharmProjects\\Cru-Wine\\CRU\\"
os.chdir(path)
winefile = 'Missing2.csv'
    #'EmpireWine-wines-new.csv'
missf = 'Missing3.csv'
lostwines = []
encoding = 'UTF-8'

connectionString = ("Driver={SQL Server Native Client 11.0};"
                    "Server=ASUS\SQLEXPRESS;"
                    "Database=WINELOGIC;"
                    "Trusted_Connection=yes;")
cnxn = pyodbc.connect(connectionString)
cursor = cnxn.cursor()


def select_csv_wines(winefile):
    wines = []
    with open(winefile, 'r', encoding='utf8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for line in reader:
            wines.append(line)

    return wines


def select_country_index(wine):
    co = wine['Country']

    cursor.execute('''IF NOT EXISTS (SELECT * FROM [Country] WHERE [Country] = ?)
                        INSERT INTO Country (Country) VALUES (?)''', co, co)
    cursor.execute("SELECT ID_country FROM Country WHERE Country = ?", co)
    results = cursor.fetchall()
    cnxn.commit()
    id_country = int(results[0][0])

    return id_country


def select_region_index(wine, id_country):
    re = wine['Region']

    try:
        cursor.execute("SELECT ID_Region FROM Region WHERE region = ?", re)
        results1 = cursor.fetchall()
        id_region = int(results1[0][0])
    except IndexError:
        cursor.execute("SELECT ID_Region, Region FROM Region WHERE ID_Country = ?", id_country)
        results = cursor.fetchall()
        res = [r[1] for r in results]
        best = difflib.get_close_matches(re, res, n=1, cutoff=0.7)
        if len(best) == 1:
            for k, v in results:
                if v == best[0]:
                    id_region = k
        else:
            dts = (id_country, re)
            cursor.execute("INSERT INTO Region (ID_Country, Region) VALUES (?,?)", dts)
            cursor.execute("SELECT ID_Region FROM Region WHERE Region = ?", re)
            resultsA = cursor.fetchall()
            id_region = int(resultsA[0][0])

        cnxn.commit()

    print(f'ID of {re} is {id_region}')

    return id_region


def select_subregion_index(wine, id_region):
    sr = wine['Subregion']

    try:
        cursor.execute("SELECT ID_Subregion FROM Subregion WHERE Subregion = ?", sr)
        results1 = cursor.fetchall()
        id_subregion = int(results1[0][0])
    except IndexError:
        cursor.execute("SELECT ID_Subregion, Subregion FROM Subregion WHERE ID_Region = ?", id_region)
        results = cursor.fetchall()
        res = [r[1] for r in results]
        best = difflib.get_close_matches(sr, res, n=1, cutoff=0.7)
        if len(best) == 1:
            for k, v in results:
                if v == best[0]:
                    id_subregion = k
        else:
            dts = (id_region, sr)
            cursor.execute("INSERT INTO Subregion (ID_Region, Subregion) VALUES (?,?)", dts)
            cursor.execute("SELECT ID_Subregion FROM Subregion WHERE Subregion = ?", sr)
            resultsA = cursor.fetchall()
            id_subregion = int(resultsA[0][0])

        cnxn.commit()

    print(f'ID of {sr} is {id_subregion}')

    return id_subregion


def select_producer_index(wine, id_region):
    pr = wine['Producer']

    try:
        cursor.execute("SELECT ID_Producer FROM Producer WHERE Producer = ?", pr)
        results1 = cursor.fetchall()
        if len(results1) > 0:
            id_producer = int(results1[0][0])
        else:
            cursor.execute("SELECT ID_Producer, Producer FROM Producer WHERE ID_Region = ?", id_region)
            results = cursor.fetchall()
            res = [r[1] for r in results]
            best = difflib.get_close_matches(pr, res, n=1, cutoff=0.8)
            if len(best) == 1:
                for k, v in results:
                    if v == best[0]:
                        id_producer = k
            else:
                dts = (id_region, pr)
                cursor.execute("INSERT INTO Producer (ID_Region, Producer) VALUES (?,?)", dts)
                cursor.execute("SELECT ID_Producer FROM Producer WHERE Producer = ?", pr)
                resultsA = cursor.fetchall()
                id_producer = int(resultsA[0][0])
    except:
        print('No producer')

    cnxn.commit()

    print(f'ID of {pr} is {id_producer}')

    return id_producer


def update_full_name(wine, id_region, id_producer):
    pfn = wine['Producer_Full']
    if pfn:
        dt1 = (id_producer, id_region)
        cursor.execute("SELECT ID_Producer, Producer_Full_Name FROM Producer WHERE ID_Producer = ? AND ID_Region = ?",
                       dt1)
        results = cursor.fetchall()
        res = results[0][1]
        if res is None:
            dt2 = (pfn, id_producer, id_region)
            cursor.execute("UPDATE Producer SET Producer_Full_Name = ? WHERE ID_Producer = ? AND ID_Region = ?", dt2)
            print(f'Full name is {pfn}')
        else:
            pass
    else:
        pass

    cnxn.commit()


def select_winetype_index(wine, id_producer, id_subregion):
    tl = wine['Title']
    cl = wine['Color']

    try:
        dts = (id_producer, tl, cl)
        cursor.execute("SELECT ID_Wine FROM Wines_Types WHERE ID_Producer = ? AND Title = ? AND Color = ?", dts)
        results1 = cursor.fetchall()
        if len(results1) > 1:
            id_winetype = int(results1[0][0])
        else:
            dd = (id_producer, cl)
            cursor.execute("SELECT ID_Wine, Title FROM Wines_Types WHERE ID_Producer = ? AND Color = ?", dd)
            results = cursor.fetchall()
            res = [r[1] for r in results]
            best = difflib.get_close_matches(tl, res, n=1, cutoff=0.9)
            if len(best) == 1:
                for k, v in results:
                    if v == best[0]:
                        id_winetype = k
            else:
                ds = (id_producer, id_subregion, tl, cl)
                cursor.execute("INSERT INTO Wines_Types (ID_Producer, ID_Subregion, Title, Color) VALUES (?,?,?,?)", ds)
                dc = (id_producer, tl, cl)
                cursor.execute("SELECT ID_Wine FROM Wines_Types WHERE ID_Producer = ? AND Title = ? AND Color = ?", dc)
                resultsA = cursor.fetchall()
                id_winetype = int(resultsA[0][0])
                cnxn.commit()
    except:
        print(f' Error with wine_type {tl}')

    print(f'ID of {tl} is {id_winetype}')

    return id_winetype


def update_wine_class(wine, id_producer, id_winetype):
    cl = wine['Classification']
    if cl:
        dt1 = (id_producer, id_winetype)
        cursor.execute("SELECT ID_Wine, Class FROM Wines_Types WHERE ID_Producer = ? AND ID_Wine = ?", dt1)
        results = cursor.fetchall()
        res = results[0][1]
        if res is None:
            dt2 = (cl, id_producer, id_winetype)
            cursor.execute("UPDATE Wines_Types SET Class = ? WHERE ID_Producer = ? AND ID_Wine = ?", dt2)
            print(f'added {cl}')
        else:
            pass
    else:
        pass

    cnxn.commit()


def select_winebtl_index(wine, id_winetype):
    ye = wine['Year']

    cursor.execute("SELECT ID_WineB FROM Wine_Bottle WHERE ID_Wine = ? AND Year = ?", (id_winetype, ye))
    results = cursor.fetchall()

    if len(results) == 0:
        dts = (id_winetype, ye)
        cursor.execute("INSERT INTO Wine_Bottle (ID_Wine, Year) VALUES (?,?)", dts)
        cursor.execute("SELECT ID_WineB FROM Wine_Bottle WHERE ID_Wine = ? AND Year = ?", (id_winetype, ye))
        resultsA = cursor.fetchall()
        id_winebtl = int(resultsA[0][0])
        cnxn.commit()
    else:
        id_winebtl = int(results[0][0])

    print(f'ID of bottle of {ye} is {id_winebtl}')

    return id_winebtl


def update_alcohol(wine, id_winebtl):
    al = wine['Alcohol']
    if al:
        cursor.execute("SELECT ID_WineB, Alcohol FROM Wine_Bottle WHERE ID_WineB = ?", id_winebtl)
        results = cursor.fetchall()
        res = results[0][1]
        if res is None:
            dt2 = (al, id_winebtl)
            cursor.execute("UPDATE Wine_Bottle SET Alcohol = ? WHERE ID_WineB = ?", dt2)
            print(f'added {al}')
        else:
            pass
    else:
        pass

    cnxn.commit()


def update_wine_grapes(wine, id_winebtl):
    gr = wine['Grapes']
    if gr:
        cursor.execute("SELECT ID_WineB, Grapes FROM Wine_Bottle WHERE ID_WineB = ?", id_winebtl)
        results = cursor.fetchall()
        res = results[0][1]
        if res is None:
            dt2 = (gr, id_winebtl)
            cursor.execute("UPDATE Wine_Bottle SET Grapes = ? WHERE ID_WineB = ?", dt2)
            print(f'added {gr}')
        else:
            pass
    else:
        pass

    cnxn.commit()


def update_maturity(wine, id_winebtl):
    ma = wine['Maturity']
    if ma:
        cursor.execute("SELECT ID_WineB, Maturity FROM Wine_Bottle WHERE ID_WineB = ?", id_winebtl)
        results = cursor.fetchall()
        res = results[0][1]
        if res is None:
            dt2 = (ma, id_winebtl)
            cursor.execute("UPDATE Wine_Bottle SET Maturity = ? WHERE ID_WineB = ?", dt2)
            print(f'added {ma}')
        else:
            pass
    else:
        pass

    cnxn.commit()


def update_wine_description(wine, id_winebtl):
    dsc = wine['Description']
    if dsc:
        cursor.execute("SELECT ID_WineB, Description FROM Wine_Bottle WHERE ID_WineB = ?", id_winebtl)
        results = cursor.fetchall()
        res = results[0][1]
        if res is None:
            dt2 = (dsc, id_winebtl)
            cursor.execute("UPDATE Wine_Bottle SET Description = ? WHERE ID_WineB = ?", dt2)
            print(f'added {dsc}')
        else:
            pass
    else:
        pass

    cnxn.commit()


def select_currency_index(wine):
    curr = wine['Currency']
    tax = wine['Tax']
    cursor.execute("SELECT ID_Currency FROM Currencies WHERE Currency = ? AND Tax = ?", (curr, tax))
    results = cursor.fetchall()
    id_currency = int(results[0][0])

    print(f'Currency is {id_currency}')

    return id_currency


def select_store_country_index(wine):
    stcn = wine['Store_Co']

    cursor.execute("SELECT ID_country FROM Country WHERE Country = ?", stcn)
    results = cursor.fetchall()

    if len(results) == 0:
        cursor.execute("INSERT INTO Country (Country) VALUES (?)", stcn)
        cursor.execute("SELECT ID_country FROM Country WHERE Country = ?", stcn)
        resultsA = cursor.fetchall()
        id_stcountry = int(resultsA[0][0])
        cnxn.commit()

    else:
        id_stcountry = int(results[0][0])

    return id_stcountry


def select_store_index(wine, id_stcountry):
    st = wine['Store']
    ci = wine['Store_Ci']

    cursor.execute("SELECT ID_Store FROM Stores WHERE Store = ?", st)
    results = cursor.fetchall()

    if len(results) == 0:
        dts = (id_stcountry, st, ci)
        cursor.execute("INSERT INTO Stores (ID_Country, Store, City) VALUES (?,?,?)", dts)
        cursor.execute("SELECT ID_Store FROM Stores WHERE Store = ?", st)
        resultsA = cursor.fetchall()
        id_store = int(resultsA[0][0])
        cnxn.commit()
    else:
        id_store = int(results[0][0])

    return id_store


def select_price_index(wine, id_winebtl, id_store, id_currency):
    sz = wine['Size']
    pr = wine['Price']
    dt = wine['Date']

    dts = (id_winebtl, id_store, sz, id_currency, pr, dt)
    cursor.execute(
        "SELECT * FROM Prices WHERE ID_WineB =? AND ID_Store = ? AND Size =? AND ID_Currency =? AND Price =? AND Date = ?",
        dts)
    results = cursor.fetchall()

    if len(results) == 0:
        cursor.execute("INSERT INTO Prices (ID_WineB, ID_Store, Size, ID_Currency,Price, Date) VALUES (?,?,?,?,?,?)",
                       dts)
    else:
        pass

    cnxn.commit()

    print('Bottle in shop!')

    return results


def pic_inserting(wine, id_winebtl):
    pic = wine['Pic_Name']
    pict = path + pic

    if os.path.exists(pict):
        try:
            dt = (pic, id_winebtl)
            with open(pict, 'rb') as photo_file:
                pho = photo_file.read()

            dtp = (pho, id_winebtl)

            cnxn = pyodbc.connect(connectionString)
            cursor = cnxn.cursor()

            cursor.execute("UPDATE Wine_Bottle SET Pic_Name = ? WHERE ID_WineB = ?", dt)
            cursor.execute("UPDATE Wine_Bottle SET Bottle_Pic = ? WHERE ID_WineB = ?", dtp)
            cnxn.commit()
            print('Image inserts')
        except:
            print('Error Image Mistake')
    else:
        dt = (pic, id_winebtl)
        cnxn = pyodbc.connect(connectionString)
        cursor = cnxn.cursor()
        cursor.execute("UPDATE Wine_Bottle SET Pic_Name = ? WHERE ID_WineB = ?", dt)
        cnxn.commit()


if __name__ == '__main__':
    wines = select_csv_wines(winefile)
    for wine in wines:
        print(wine['Title'])
        try:
            id_country = select_country_index(wine)
            id_region = select_region_index(wine, id_country)
            id_subregion = select_subregion_index(wine, id_region)
            id_producer = select_producer_index(wine, id_region)
            update_full_name(wine, id_region, id_producer)
            id_winetype = select_winetype_index(wine, id_producer, id_subregion)
            update_wine_class(wine, id_producer, id_winetype)
            id_winebtl = select_winebtl_index(wine, id_winetype)
            update_alcohol(wine, id_winebtl)
            update_wine_grapes(wine, id_winebtl)
            update_maturity(wine, id_winebtl)
            update_wine_description(wine, id_winebtl)
            pr = wine['Price']
            if pr:
                id_currency = select_currency_index(wine)
                id_stcountry = select_store_country_index(wine)
                id_store = select_store_index(wine, id_stcountry)
                results = select_price_index(wine, id_winebtl, id_store, id_currency)
            pic_inserting(wine, id_winebtl)
        except:
            print(f'Wine missing {wine}')
            lostwines.append(wine)
    if len(lostwines) > 0:
        print(len(lostwines))
        with open(missf, 'a', newline='', encoding='utf8') as fl:
            writer = csv.writer(fl, delimiter=';')
            writer.writerow(['Country', 'Region', 'Subregion', 'Producer', 'Producer_Full', 'Producer_Notes', 'Title', 'Classification', 'Color', 'Grapes', 'Wine_Notes', 'Year', 'Alcohol', 'Maturity', 'Description', 'Pic_Name', 'Size', 'Price', 'Currency', 'Tax', 'Store','Store_Co', 'Store_Ci', 'Date'])
            for w in lostwines:
                writer.writerow([w['Country'], w['Region'], w['Subregion'], w['Producer'], w['Producer_Full'],
                                 w['Producer_Notes'], w['Title'], w['Classification'], w['Color'], w['Grapes'],
                                 w['Wine_Notes'], w['Year'], w['Alcohol'], w['Maturity'], w['Description'],
                                 w['Pic_Name'], w['Size'], w['Price'], w['Currency'], w['Tax'],
                                 w['Store'], w['Store_Co'], w['Store_Ci'], w['Date']])
        # with open('Missing.csv', 'w', newline='', encoding='utf8') as file:
        #     writer = csv.writer(file, delimiter=';')
        #     for w in lostwines:
        #         writer.writerow(w)
    cnxn.close()
