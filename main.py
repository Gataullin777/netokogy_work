import requests
from bs4 import BeautifulSoup
import sort

url = 'https://habr.com/ru/all/'
KEYWORDS = ['дизайн', 'фото', 'web', 'python']
HOST = 'https://habr.com'

def get_html(url):
    response = requests.get(url)
    if response.ok:
        #print('ok')
        return response.content
    else:
        print(f'bad link: {url}')

def work_on_content(html):
    try:
        soup = BeautifulSoup(html, 'lxml')
        articles = soup.findAll('article', class_='tm-articles-list__item')
        for article in articles:
            try:
                text = article.find('div', class_='article-formatted-body article-formatted-body_version-1').text
                #pprint(text)
                #print('++++++++++++++++++++++++')
            except:
                text = article.find('div', class_='article-formatted-body article-formatted-body_version-2').text
                #pprint(text)
                #print('++++++++++++++++++++++++')

            number_of_coincidences = 0
            for word in KEYWORDS:
                result = sort.search(word, text)
                #print(result)

                if result == 1:
                    number_of_coincidences = 1

            if number_of_coincidences == 1:
                link = article.find('a', class_='tm-article-snippet__readmore').get('href')
                link = HOST + link
                #print(link)

                header = article.find('h2', class_='tm-article-snippet__title tm-article-snippet__title_h2').text
                #print(header)

                date = article.find('time').get('title')
                print(f'дата: {date} , заголовок: {header}, ссылка:{link} ')


            elif number_of_coincidences != 1:
                url = article.find('a', class_='tm-article-snippet__readmore').get('href')
                url = HOST + url
                html_2 = get_html(url)
                soup_2 = BeautifulSoup(html_2, 'lxml')
                text = soup_2.find('div', id='post-content-body').text
                #pprint(text)
                result = sort.search(word, text)
                #print(result)

                if result == 1:
                    link = article.find('a', class_='tm-article-snippet__readmore').get('href')
                    link = HOST + link
                    # print(link)

                    header = article.find('h2', class_='tm-article-snippet__title tm-article-snippet__title_h2').text
                    # print(header)

                    date = article.find('time').get('title')
                    print(f'дата: {date} , заголовок: {header}, ссылка:{link} ')

                else:
                    continue

    except Exception as e:
        print(e)


if __name__=='__main__':
    html = get_html(url)
    work_on_content(html)