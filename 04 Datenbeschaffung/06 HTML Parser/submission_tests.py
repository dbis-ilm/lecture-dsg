from jptest import *


@JPTest('Aufgabe 1', max_score=3, execute=[
    '''
    import requests
    from bs4 import BeautifulSoup
    ''',
    ('task-1',)
])
def test_aufgabe1(tb: JPTestBook):
    # page
    result = tb.get('page')
    test = tb.inject('''
        text = requests.get('https://de.wikipedia.org/wiki/Geschichte_des_Kinos').text
        page = BeautifulSoup(text)
    ''', 'page')

    yield test == result, 1, '`page` nicht korrekt'

    # links
    result = tb.get('links')
    test = tb.inject('''
        links = page.find('div', id='bodyContent').find_all('a')
    ''', 'links')

    yield test == result, 1, '`links` nicht korrekt'

    # refs
    result = tb.get('refs')
    test = tb.inject('''
        refs = [a['href'] for a in links if a['href'].startswith('/wiki/')]
    ''', 'refs')

    yield test == result, 1, '`refs` nicht korrekt'
