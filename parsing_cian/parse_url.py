import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Список user agents
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
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88 Safari/537.",
]

def get_driver_with_agent(user_agent):
    """
    Инициализирует драйвер с заданным user-agent.
    """
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={user_agent}')
    return webdriver.Chrome(options=options)

def close_advertisement(driver):
    """
    Если появляется всплывающая реклама, пытается найти кнопку закрытия,
    исключая элементы с data-testid="ConsultantWidgetMainButton".
    """
    xpaths = [
        "//*[contains(@class, 'close') and not(contains(@data-testid, 'ConsultantWidgetMainButton'))]",
        "//*[contains(@class, 'icon-close') and not(contains(@data-testid, 'ConsultantWidgetMainButton'))]",
        "//*[contains(@aria-label, 'Закрыть') and not(contains(@data-testid, 'ConsultantWidgetMainButton'))]"
    ]
    for xpath in xpaths:
        try:
            ad_close_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            ad_close_button.click()
            print("Реклама закрыта с xpath:", xpath)
            break
        except TimeoutException:
            continue

def close_cookies(driver):
    """
    Закрывает уведомление о куках, если оно присутствует.
    """
    try:
        cookie = driver.find_element(By.XPATH, "//div[@data-name='CookiesNotification']")
        driver.execute_script("arguments[0].style.display='none';", cookie)
        print("Уведомление о куках закрыто.")
    except Exception:
        print("Уведомление о куках не найдено или произошла ошибка при его закрытии.")

def parse_ad_links(driver, ad_links):
    """
    Парсит ссылки объявлений и добавляет новые в список ad_links.
    """
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[starts-with(@href, 'https://www.cian.ru/sale/flat/')]"))
        )
    except TimeoutException:
        print("Timeout ожидания ссылок объявлений, пытаемся собрать их вручную.")

    ads = driver.find_elements(By.XPATH, "//a[starts-with(@href, 'https://www.cian.ru/sale/flat/')]")
    if not ads:
        print("Ссылки объявлений не найдены, ждем еще 5 секунд...")
        time.sleep(5)
        ads = driver.find_elements(By.XPATH, "//a[starts-with(@href, 'https://www.cian.ru/sale/flat/')]")
        if not ads:
            print("Ссылки объявлений по-прежнему не найдены.")
            return ad_links

    for ad in ads:
        link = ad.get_attribute("href")
        if link not in ad_links:
            ad_links.append(link)
    print("Количество собранных ссылок:", len(set(ad_links)))
    return ad_links

def get_next_page_url(driver):
    """
    Находит ссылку на следующую страницу по кнопке "Дальше".
    Если кнопка не найдена, возвращает None.
    """
    next_buttons = driver.find_elements(By.XPATH, "//a[.//span[contains(text(),'Дальше')]]")
    if not next_buttons:
        print("Кнопка 'Дальше' не найдена. Завершаем парсинг.")
        return None
    next_page_url = next_buttons[0].get_attribute("href")
    return next_page_url

start_url = (
    "https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&from_developer=1&hand_over=1&object_type%5B0%5D=2&offer_type=flat&only_flat=1&region=1&room1=1&room2=1&room3=1&room4=1"
)

# Инициализируем драйвер с случайным user-agent
current_user_agent = random.choice(user_agents)
driver = get_driver_with_agent(current_user_agent)
driver.get(start_url)

ad_links = []

while True:
    # Ждем полной загрузки страницы
    WebDriverWait(driver, 20).until(lambda d: d.execute_script("return document.readyState") == "complete")
    # 1. Проверяем и закрываем рекламу
    close_advertisement(driver)
    # 2. Закрываем уведомление о куках
    close_cookies(driver)
    
    time.sleep(1)
    ad_links = []
    # 3. Парсинг ссылок объявлений
    ad_links = parse_ad_links(driver, ad_links)
    # Записываем ссылки в файл перед переходом на следующую страницу
    with open('url.txt', mode='a', encoding='utf-8') as f:
        for link in ad_links:
            f.write(link + "\n")
    print("Ссылки записаны в файл 'url'.")

    # 4. Переход на следующую страницу
    next_page_url = get_next_page_url(driver)
    print("Парсинг завершён. Теперь:", driver.current_url)
    if not next_page_url:
        # Если парсинг завершается, выводим последнюю ссылку (текущий URL)
        print("Парсинг завершён. Последняя ссылка:", driver.current_url)
        break

    driver.get(next_page_url)
    time.sleep(3)

driver.quit()
