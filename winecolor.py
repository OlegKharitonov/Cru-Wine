
def wine_color(page):
    if 'red' in page:
        color = 'red'
    elif 'white' in page:
        color = 'white'
    elif 'sparkling' in page:
        color = 'sparkling'
    elif 'sweet' in page:
        color = 'sweet'
    elif 'tinto' in page:
        color = 'red'
    elif 'blanco' in page:
        color = 'white'
    elif 'espumoso' in page:
        color = 'sparkling'
    elif 'rosado' in page:
        color = 'rose'
    elif 'dulce' in page:
        color = 'sweet'
    else:
        color = ''

    return color