import requests # type: ignore
from bs4 import BeautifulSoup as bs
import csv
import random
import time
import func


# file_out = open('output.csv', mode='w', encoding='utf-8', newline='')
# writer = csv.writer(file_out)
# writer.writerow(['ЖК', 'Цена', 'Количество комнат', 'Количество санузлов', 
#                  'Общая площадь', 'Площадь кухни', 'Жилая площадь', 'Наличие балкона', 'Этаж', 'Высота потолков', 'Отделка'])
# file_out.close()


file_in = open('url.txt')
input = file_in.readlines()

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7; SM-G950F Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85 Mobile Safari/537.",
    "Mozilla/5.0 (Windows NT 10; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88 Safari/537.",
]

session = requests.Session()

f_ready = open('url_ready.txt', mode='r')
f_fucked = open('url_fucked.txt', mode='r')

url_ready = f_ready.readlines()
url_fucked = f_fucked.readlines()

for i in range(len(url_ready)):
    url_ready[i] = url_ready[i].strip()

for i in range(len(url_fucked)):
    url_fucked[i] = url_fucked[i].strip()

f_ready.close()
f_fucked.close()

for url in input:
    
    url = url.strip()
    
    file_out = open('flats.csv', mode='a', encoding='utf-8', newline='')
    writer = csv.writer(file_out)
    
    f_ready = open('url_ready.txt', mode='a')
    f_fucked = open('url_fucked.txt', mode='a')
    
    if url in url_ready:
        continue
    
    if url in url_fucked:
        continue
    
    time.sleep(random.randint(2, 5))
    
    header = {
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control':'no-cache',
        'dnt': '1',
        'pragma': 'no-cache',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': random.choice(user_agents)}
    
    session.headers.update(header)
    attempt = 0
    # Отправляем запрос с обработкой ошибки 429
    while True:
        if attempt > 0:
            print('Пробую ещё раз')
        response = session.get(url.strip())
        time.sleep(5)
        if response.status_code == 429:
            print(f'Ошибка 429. Почти печаль беда катастрофа')
            attempt += 1
        else:
            break

    if response.status_code == 200:
        soup = bs(response.text, 'html.parser')


        jk = func.parse_jk(response.text)
        price = func.parse_price(response.text)
        rooms = func.parse_rooms(response.text)
        bathrooms = func.parse_bathroom(response.text)
        total_area = func.parse_total_area(response.text)
        kitchen_area = func.parse_kitchen_area(response.text)
        living_area = func.parse_living_area(response.text)
        balcony = func.parse_balcony(response.text)
        floor = func.parse_floor(response.text)
        ceiling_height = func.parse_ceiling_height(response.text)
        decoration = func.parse_decoration(response.text)
        
        
        print('OK')
        writer.writerow([jk, price, rooms, bathrooms, total_area, 
                         kitchen_area, living_area, balcony, floor, ceiling_height, decoration])
        
        print('Записал')
        f_ready.write(url+'\n')
    else:
        print('ПЕЧАЛЬ БЕДА КАТАСТРОФА', url, header['user-agent'])
        f_fucked.write(url+'\n')
        print(response.status_code)