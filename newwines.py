
import os

allwines = []
nwines = []
items = []

def select_new_wines (wf, wfn, items, site):
    pth = 'E:/WINE-Project/' + site + '/'
    os.chdir(pth)

    with open(wf, 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            allwines.append(line)
        print(allwines)

    for item in items:
        print(item)
        if item not in allwines:
            nwines.append(item)

    with open(wfn, 'a') as fn:
        for it in nwines:
            fn.write(it + '\n')

    with open(wf, 'a') as f1:
        for it1 in nwines:
            f1.write(it1 + '\n')

    return nwines
