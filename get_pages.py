
mpages = []


def mix_pages(page, max_page):
    if 'empirewine.com' in page:
        for x in range(1, max_page + 1):
            mpages.append(page[0:-1] + str(x))
    elif 'bodeboca' in page:
        for x in range(1, max_page + 1):
            mpages.append(page.split('=')[0] + '=' + str(x) + '&sort' + page.split('&sort')[1])
    else:
        print('error')

    return mpages

