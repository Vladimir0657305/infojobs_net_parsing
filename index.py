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
    time.sleep(15)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    last_page = int(soup.find(
        'ul', class_='sui-MoleculePagination').find_all('li', class_='sui-MoleculePagination-item')[-2].text.strip())

    all_links = []
    wall_links = []

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


def page_data(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(15)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    title = soup.find('h1', id='prefijoPuesto').text.strip()
    company = soup.find(
        'div', class_='content-type-text').find('a').text.strip()
    prefijoPoblacion = soup.find('span', id='prefijoPoblacion').text.strip().replace(',', ' ')
    prefijoProvincia = soup.find('a', id='prefijoProvincia').text.strip()
    presencial = soup.find('ul', class_='list-default list-bullet-default small').find_all('li')[1].text.strip()
    publicada = soup.find('ul', class_='list-default list-bullet-default small').find_all('li')[2].text.strip().replace('\n', ' ')
    salario = soup.find('ul', class_='list-default list-bullet-default small').find_all('li')[3].text.strip()
    experiencia = soup.find_all('ul', class_='list-default list-bullet-default small')[1].find_all('li')[0].text.strip()
    tipo = soup.find_all('ul', class_='list-default list-bullet-default small')[1].find_all('li')[1].text.replace(',', ' ')
    estudios = soup.find('span', id='prefijoEstMin').text.strip()
    mínima = soup.find_all('ul', class_='list-default')[2].find_all('li')[1].text.strip()
    conocimientos_label = soup.find_all('ul', class_='list-default')[2].find_all(
        'li')[2].find('ul', class_='list-default list-inline').find_all('li')
    conocimientos = ''
    if conocimientos_label:
        for i in conocimientos_label:
            conocimientos += i.text.strip() + ' '
    requisitos = soup.find_all('ul', class_='list-default')[2].find_all('li')[-1].text.strip()
    descripcion = soup.find('div', id='prefijoDescripcion1').text.strip()
    tipo_de_industria = soup.find('div', class_='highlight-text border-top padding-top margin-top').find('ul', class_='list-default').find_all('li')[0].text.strip()
    categoria = soup.find('div', class_='highlight-text border-top padding-top margin-top').find('ul', class_='list-default').find_all('li')[1].text.strip()
    nivel = soup.find('div', class_='highlight-text border-top padding-top margin-top').find('ul', class_='list-default').find_all('li')[2].text.strip()
    personal_a_cargo = soup.find('div', class_='highlight-text border-top padding-top margin-top').find('ul', class_='list-default').find_all('li')[3].text.strip()
    numero_de_vacantes = soup.find('div', class_='highlight-text border-top padding-top margin-top').find('ul', class_='list-default').find_all('li')[4].text.strip()
    salario2 = soup.find('div', class_='highlight-text border-top padding-top margin-top').find('ul', class_='list-default').find_all('li')[-1].text.strip()
    inscritos = soup.find(
        'strong', id='candidate_application_message').text.strip()
    
    
    print('DATA====>', url, title, company, prefijoPoblacion,
          prefijoProvincia, presencial, publicada, salario, experiencia, tipo, estudios, mínima, conocimientos, requisitos, descripcion, tipo_de_industria, categoria, nivel, personal_a_cargo, numero_de_vacantes, salario2, inscritos)
    
    driver.quit()
    data = {'url': url, 'title': title, 'company': company, 'prefijoPoblacion': prefijoPoblacion, 'prefijoProvincia': prefijoProvincia, 'presencial': presencial, 'publicada': publicada, "salario": salario, 'experiencia': experiencia, 'tipo': tipo, 'estudios': estudios, 'mínima': mínima,
            'conocimientos': conocimientos, 'requisitos': requisitos, 'descripcion': descripcion, 'tipo_de_industria': tipo_de_industria, 'categoria': categoria, 'nivel': nivel, 'personal_a_cargo': personal_a_cargo, 'numero_de_vacantes': numero_de_vacantes, 'salario2': salario2, 'inscritos': inscritos}
    return data








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

# Сохраняем результаты в CSV-файл


def write_csv(data):
    with open('jobs_data.csv', 'a', newline='', encoding='utf-8-sig') as file:
        # fieldnames = ['Name', 'Price']
        writer = csv.writer(file)
        # writer.writeheader()
        writer.writerow((data['url'], data['title'],
                        data['company'], data['prefijoPoblacion'], data['prefijoProvincia'], data['presencial'], data['publicada'], data["salario"], data['experiencia'], data['tipo'], data['estudios'], data['mínima'], data['conocimientos'], data['requisitos'], data['descripcion'], data['tipo_de_industria'], data['categoria'], data['nivel'], data['personal_a_cargo'], data['numero_de_vacantes'], data['salario2'], data['inscritos']))

def main():
    page = 1
    global last_page
    all_data = []
    # while True:
    #     if page == 1:
    #         links = get_links(f'https://www.infojobs.net/ofertas-trabajo?keyword=Instalador%2Fa%20de%20paneles%20solares%20fotovoltaicos')
    #     else:
    #         get_links(
    #             f'https://www.infojobs.net/ofertas-trabajo?keyword=Instalador%2Fa%20de%20paneles%20solares%20fotovoltaicos&normalizedJobTitleIds=7411_75b63949-1b93-4bf2-a777-ccf978dc3e8a&provinceIds=&cityIds=&teleworkingIds=&categoryIds=&workdayIds=&educationIds=&segmentId=&contractTypeIds=&page={page}&sortBy=RELEVANCE&onlyForeignCountry=false&countryIds=&sinceDate=ANY&subcategoryIds=')
    #     print('PAGE===>', page, last_page)
    #     if page > last_page:
    #         break
    #     else:
    #         page += 1

    # cur_data = page_data('https://www.infojobs.net/tortosa/fotovotaica-montadores-placas-electricistas-tortosa/of-ie17a00bb064075938f12208a404059')
    cur_data = page_data('https://www.infojobs.net/xirivella/instalador-placas-solares/of-if65571f10c4a168c42cf5efddf294d')
    all_data.append(cur_data)
    write_csv(cur_data)

if __name__ =='__main__':
    main()
