import sys
import os
import SQLiteDataBase as myDB

import requests
from bs4 import BeautifulSoup

URL = 'https://playtoearn.net/blockchaingames'
HEADERS = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
}
PATH = ''
def get_html(url, params = None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def work_with_url(html, index, i , iterator, cats_info):
    htmlForPagination = html
    soup = BeautifulSoup(html, 'html.parser')

    items = soup.find('table', class_='table table-bordered mainlist')
    iterator = 2
    for item in items.find_all('div', class_='dapp_profilepic dapp_profilepic_list'):
        i+=1
        print(iterator)
        try:
            allItems = items.find_all('tr')
            allItems_td = allItems[iterator].find_all('td')
            name = allItems_td[2].find('img').get('alt')
            img = allItems_td[2].find('img').get('src')  # получаем ссылку на файл фотографии
            saveImg(img, i)
            game_satus = allItems_td[6].get_text('title')  # получаем статус игры
            print(img)
            print(game_satus)
            print(name)
            cats_info.append((int(i), f'{i}/saveImg', name, game_satus))
            #print(cats_info)
            iterator += 1
        except:
            break

    index+=1
    pagination(htmlForPagination, index, i, iterator, cats_info)

def pagination(html, index,i, iterator, cats_info):
    print(cats_info)
    if(index==25):
        myDB.executeSqlDataBase(cats_info)
        sys.exit(1)
    url = "https://playtoearn.net/blockchaingames?sort=socialscore_24h&direction=desc&page=" + str(index)
    print(url)
    html = get_html(url)
    work_with_url(html.text, index, i , iterator, cats_info)

def saveImg(img,i):
    if not os.path.exists('saveImg'):
        os.mkdir('saveImg')
    img_data = requests.get(img, verify=True).content
    #print(img_data)
    with open(f'saveImg/'+f'{i}.img', 'wb') as handler:
        handler.write(img_data)
    handler.close()

def parse():
    html = get_html(URL)
    index = 1
    i = 0
    iterator = 2
    cats_info = []
    if html.status_code == 200:
        work_with_url(html.text, index, i , iterator, cats_info)
    else: print('Error')


#main
parse()