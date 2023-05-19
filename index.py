import requests
from bs4 import BeautifulSoup

headers = {
    'accept': 'application/json charset = utf-8',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
}

def get_links(url):
    # response = requests.get(url=url, headers=headers, proxies=proxies)
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find('ul', class_='ij-List ij-List--vertical ij-List--spaced').find_all(
        'li').find('h2').text.strip()
    location = soup.find('table', class_='ui celled striped table').find(
        'tbody').find_all('tr')[2].find_all('td')[1].text.strip()

    print(f'{ip}\nLocation: {location}')

def main():
    page = 1
    url = f'https://www.infojobs.net/ofertas-trabajo?keyword=Instalador%2Fa%20de%20paneles%20solares%20fotovoltaicos&normalizedJobTitleIds=7411_75b63949-1b93-4bf2-a777-ccf978dc3e8a&provinceIds=&cityIds=&teleworkingIds=&categoryIds=&workdayIds=&educationIds=&segmentId=&contractTypeIds=&page={page}&sortBy=RELEVANCE&onlyForeignCountry=false&countryIds=&sinceDate=ANY&subcategoryIds='
    get_links(url)

if __name__ =='__main__':
    main()