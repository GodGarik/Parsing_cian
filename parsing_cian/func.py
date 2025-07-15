import requests # type: ignore
from bs4 import BeautifulSoup as bs
import csv
import random
import time


def parse_price(text):
    
    soup = bs(text, 'html.parser')
    
    # Находим div с нужным data-testid

    price_div = soup.find('div', {'data-testid': 'price-amount'})
    # Находим span внутри этого div
    price_span = price_div.find('span')
    # Извлекаем текст и убираем лишние символы
    price_text = price_span.get_text(strip=True)
    price_value = price_text.replace('₽', '').strip()

    return price_value



def parse_rooms(text):
    
    soup = bs(text, 'html.parser')
    
    # Находим div с нужным data-testid
    price_div = soup.find('div', {'data-name': 'OfferTitleNew'})

    # Находим span внутри этого div
    title_h1 = soup.find('h1', class_='a10a3f92e9--title--vlZwT')
    title_text = title_h1.get_text(strip=True)

    # Разделяем текст по пробелам и ищем нужную часть
    parts = title_text.split()
    room_type = next((part for part in parts if 'комн.' in part), None)

    return room_type


def parse_jk(text):
    
    soup = bs(text, 'html.parser')
    
    
    # Находим нужный div
    parent_div = soup.find('div', {'data-name': 'ParentNew'})
    if parent_div is not None:
        jkk_name = parent_div.find('a').text
        return jkk_name



def parse_bathroom(text):
    
    soup = bs(text, 'html.parser')
    
    # Находим все элементы с нужным классом
    items = soup.find_all('div', class_='a10a3f92e9--item--qJhdR')

    # Перебираем найденные элементы
    for item in items:
        # Находим все <p> внутри текущего элемента
        paragraphs = item.find_all('p')
        if len(paragraphs) > 1:
            # Проверяем текст первого <p>
            if "Санузел" in paragraphs[0].get_text(strip=True):
                # Если нашли нужный элемент, выводим текст второго <p>
                return paragraphs[1].get_text(strip=True)


def parse_total_area(text):
    
    soup = bs(text, 'html.parser')
    
    # Находим все элементы с нужным классом
    items = soup.find_all('div', class_='a10a3f92e9--item--qJhdR')

    # Перебираем найденные элементы
    for item in items:
        # Находим все <p> внутри текущего элемента
        paragraphs = item.find_all('p')
        if len(paragraphs) > 1:
            # Проверяем текст первого <p>
            if "Общая площадь" in paragraphs[0].get_text(strip=True):
                # Если нашли нужный элемент, выводим текст второго <p>
                return (paragraphs[1].get_text(strip=True)).split()[0]
            
            
def parse_kitchen_area(text):
    
    soup = bs(text, 'html.parser')
    
    # Находим все элементы с нужным классом
    items = soup.find_all('div', class_='a10a3f92e9--item--qJhdR')

    # Перебираем найденные элементы
    for item in items:
        # Находим все <p> внутри текущего элемента
        paragraphs = item.find_all('p')
        if len(paragraphs) > 1:
            # Проверяем текст первого <p>
            if "Площадь кухни" in paragraphs[0].get_text(strip=True):
                # Если нашли нужный элемент, выводим текст второго <p>
                return (paragraphs[1].get_text(strip=True)).split()[0]
            

def parse_living_area(text):
    
    soup = bs(text, 'html.parser')
    
    # Находим все элементы с нужным классом
    items = soup.find_all('div', class_='a10a3f92e9--item--qJhdR')

    # Перебираем найденные элементы
    for item in items:
        # Находим все <p> внутри текущего элемента
        paragraphs = item.find_all('p')
        if len(paragraphs) > 1:
            # Проверяем текст первого <p>
            if "Жилая площадь" in paragraphs[0].get_text(strip=True):
                # Если нашли нужный элемент, выводим текст второго <p>
                return (paragraphs[1].get_text(strip=True)).split()[0]
            
            
def parse_balcony(text):
    
    soup = bs(text, 'html.parser')
    
    # Находим все элементы с нужным классом
    items = soup.find_all('div', class_='a10a3f92e9--item--qJhdR')

    # Перебираем найденные элементы
    for item in items:
        # Находим все <p> внутри текущего элемента
        paragraphs = item.find_all('p')
        if len(paragraphs) > 1:
            # Проверяем текст первого <p>
            if "Жилая площадь" in paragraphs[0].get_text(strip=True):
                # Если нашли нужный элемент, выводим текст второго <p>
                return (paragraphs[1].get_text(strip=True))
            else:
                return 'Балкона нет'
            
            
def parse_ceiling_height(text):
    
    soup = bs(text, 'html.parser')
    
    # Находим все элементы с нужным классом
    items = soup.find_all('div', class_='a10a3f92e9--item--qJhdR')

    # Перебираем найденные элементы
    for item in items:
        # Находим все <p> внутри текущего элемента
        paragraphs = item.find_all('p')
        if len(paragraphs) > 1:
            # Проверяем текст первого <p>
            if "Высота потолков" in paragraphs[0].get_text(strip=True):
                # Если нашли нужный элемент, выводим текст второго <p>
                return (paragraphs[1].get_text(strip=True)).split()[0]
            
            
def parse_decoration(text):
    
    soup = bs(text, 'html.parser')
    
    # Находим все элементы с нужным классом
    items = soup.find_all('div', class_='a10a3f92e9--item--qJhdR')

    # Перебираем найденные элементы
    for item in items:
        # Находим все <p> внутри текущего элемента
        paragraphs = item.find_all('p')
        if len(paragraphs) > 1:
            # Проверяем текст первого <p>
            if "Отделка" in paragraphs[0].get_text(strip=True):
                # Если нашли нужный элемент, выводим текст второго <p>
                return paragraphs[1].get_text(strip=True)
            
            
def parse_floor(text):
    
    soup = bs(text, 'html.parser')
    
    # Ищем все элементы div с классом 'a10a3f92e9--text--eplgM'
    divs = soup.find_all('div', class_='a10a3f92e9--text--eplgM')

    for div in divs:
        spans = div.find_all('span')
        for span in spans:
            if 'из' in span.text:
                # Заменяем " из " на "/"
                result = span.text.strip().replace(" из ", "/")
                return result