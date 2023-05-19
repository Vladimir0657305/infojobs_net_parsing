from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time
import csv
import requests
from bs4 import BeautifulSoup

headers = {
    'accept': 'application/json charset = utf-8',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
}
last_page = 0

def get_links(url):
    global last_page
    
    options = Options()
    options.add_argument('--headless')

    # driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome()
    driver.get(url)
    # wait = WebDriverWait(driver, 20)
    time.sleep(30)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    last_page = int(soup.find(
        'ul', class_='sui-MoleculePagination').find_all('li', class_='sui-MoleculePagination-item')[-2].text.strip())
    print('QQQQQQ===>', last_page)

    all_links = []

    while True:
        # Получение высоты страницы
        page_height = driver.execute_script('return document.documentElement.scrollHeight;')
        print('page_height====>', page_height)

        # Получение высоты видимой области окна браузера
        window_height = driver.execute_script('return window.innerHeight;')
        print('window_height====>', window_height)

        # Получение текущего положения полосы прокрутки
        scroll_y = driver.execute_script('return window.scrollY;')
        print('scroll_y===>', scroll_y)

        # Проверка условия для выполнения скролла
        if scroll_y + window_height <= page_height:
            # driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight);')
            driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(1)

            new_soup = BeautifulSoup(driver.page_source, 'html.parser')
            new_links = new_soup.find(
                'ul', class_='ij-List ij-List--vertical ij-List--spaced').find_all('li', class_='ij-List-item')
            for new_link in new_links:
                try:
                    link = new_link.find(
                        'h2', class_='ij-OfferCardContent-description-title').find('a', href=True).get('href').split('?')[0]
                    t = 'https:' + link
                    if t not in all_links:  # Проверка на дублирование ссылок
                        all_links.append(t)
                except:
                    pass
            
            if scroll_y + window_height >= page_height: 
                driver.quit()
                break
        else:
            break
    
    write_csv_links(all_links)
    return all_links





    # response = requests.get(url=url, headers=headers, proxies=proxies)
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find('ul', class_='ij-List ij-List--vertical ij-List--spaced').find_all(
        'li').find('h2').text.strip()
    location = soup.find('table', class_='ui celled striped table').find(
        'tbody').find_all('tr')[2].find_all('td')[1].text.strip()

    print(f'{ip}\nLocation: {location}')


def write_csv_links(data):
    counter = 1
    with open('links.csv', 'a', newline='', encoding='utf-8') as file:
        # fieldnames = ['Name', 'Price']
        writer = csv.writer(file)
        # writer.writeheader()
        for i in data:
            writer.writerow([i])
            print('SAVE=>', counter, i)
            counter += 1

def main():
    page = 1
    global last_page
    # url = f'https://www.infojobs.net/ofertas-trabajo?keyword=Instalador%2Fa%20de%20paneles%20solares%20fotovoltaicos'
    while True:
        links = get_links(
            f'https://www.infojobs.net/ofertas-trabajo?keyword=Instalador%2Fa%20de%20paneles%20solares%20fotovoltaicos')
        print('PAGE===>', page, last_page)
        if page > last_page:
            break
        else:
            page += 1
    

if __name__ =='__main__':
    main()