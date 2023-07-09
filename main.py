import requests
import json
from bs4 import BeautifulSoup
from fake_headers import Headers

headers = Headers(os='win', browser='chrome')
vacancy = []
hh_new_vacancy = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'

def get_page(url):
    return requests.get(url, headers=headers.generate())

def vacancies_links(url):
    vacancy_html = get_page(url).text
    soup = BeautifulSoup(vacancy_html, features='lxml')
    links_tag = soup.find_all(class_="serp-item__title")
    for link_tag in links_tag:
        link = link_tag['href']
        find_django_flask(link)


def find_django_flask(vacancy_link):
    vacancy_html = get_page(vacancy_link).text
    soup = BeautifulSoup(vacancy_html, features='lxml')
    description = soup.find(class_="g-user-content").text
    django = description.find('Django')
    flask = description.find('Flask')
    if django != -1 or flask != -1:
        parse_vacancy_info(vacancy_link)

def parse_vacancy_info(vacancy_link):
    vacancy_html = get_page(vacancy_link).text
    soup = BeautifulSoup(vacancy_html, features='lxml')
    link = vacancy_link
    vacancy_title = soup.find(class_="vacancy-title")
    salary = vacancy_title.find('span').text
    company_name = soup.find(class_="vacancy-company-name").text
    city_tag = soup.find(class_="bloko-link bloko-link_kind-tertiary bloko-link_disable-visited")
    if city_tag == None:
        city = None
    else:
        address = city_tag.find('span').text.split()
        city = address[0]
    result = {
        'link':link,
        'salary':salary,
        'company_name':company_name,
        'city':city
    }
    vacancy.append(result)

def save_in_json():
    with open("vacancy_info.json", "a") as f:
        f.write(json.dumps(vacancy, ensure_ascii=False))

if __name__ == '__main__':
    vacancies_links(hh_new_vacancy)
    save_in_json()