import pandas as pd
import os

path = "C:\\Users\\user\\PycharmProjects\\Cru-Wine\\CRU\\"
os.chdir(path)

f1 = path + 'EmpireWine-wines.csv'
f2 = path + 'EmpireWine-wines-new.csv'
nf = path + 'EmpireWine_W.csv'

def csvfile_plus_csvfile( f1, f2, nf):
    a = pd.read_csv(f1, delimiter = ';', encoding = 'UTF-8')
    b = pd.read_csv(f2, delimiter = ';', encoding = 'UTF-8')
    new = a.append(b)
    new.to_csv(nf, index = False, encoding = 'UTF-8', sep = ';')

