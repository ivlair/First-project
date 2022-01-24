import csv
import datetime

import requests
from bs4 import BeautifulSoup

CSV = 'condo.csv'
HOST = 'https://www.avito.ru/'
URL = 'https://www.avito.ru/solnechnogorsk/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('div', class_='iva-item-content-rejJg')
    condo = []

    for item in items:
        if 'solnechnogorsk' in item.find('a', class_='iva-item-sliderLink-uLz1v').get('href'):
            condo.append(
                {
                    'title': item.find('div', class_='iva-item-titleStep-pdebR').get_text(strip=True).replace(u'\xa0',
                                                                                                              u' '),
                    'price': item.find('span', class_='price-price-JP7qe').get_text(
                        strip=True).replace(u'\xa0', u' '),
                    'address': item.find('span', class_='geo-address-fhHd0 text-text-LurtD text-size-s-BxGpL').get_text(
                        strip=True).replace(u'\xa0', u' ')
                }
            )
    return condo


def save_doc(items, path):
    with open(path, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название объявления', 'Стоимость', 'Адрес'])
        for item in items:
            writer.writerow([item['title'], item['price'], item['address']])

dt_now = datetime.datetime.now()
print(dt_now.year)
html = get_html(URL)
condo = get_content(html.text)
sort_condo = sorted(condo, key=lambda row: (row['address'], row['title']), reverse=False)
save_doc(sort_condo, CSV)

# html = get_html(URL)
# print(get_content(html.text))
