import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def find_hex(color):
    ua = UserAgent()
    url = 'https://alexbeals.com/projects/colorize/search.php?q='
    headers = {'User-Agent': str(ua.random)}

    source = requests.get(url+color, headers=headers)
    plain_text = source.text
    soup = BeautifulSoup(plain_text, 'lxml')

    hexcolor = soup.body.get('style').split(':')[1].strip()
    hexcolor = hexcolor.replace('#', '')
    return hexcolor
