import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

url = 'https://habr.com/ru/all/'
KEYWORDS = ['дизайн', 'фото', 'web', 'python']
HOST = 'https://habr.com'

def decor_path(path_log):
    def decorator(func):
        def new_func(*args, **kwargs):
            #print('first print')
            result = func(*args, **kwargs)
            #print('second print')
            with open(path_log, 'a', encoding='utf-8') as f:
                f.write(f'{func.__name__} - {datetime.now()} - {args} - {kwargs} \n')
            return result
        return new_func
    return decorator


def search(word, text):
    pattern_1 = rf'{word.capitalize()}'
    pattern_2 = rf'{word.lower()}'
    result_1 = re.search(pattern_1, text)
    result_2 = re.search(pattern_2, text)
    if not result_1 is None or not result_2 is None:
        return 1
    else:
        return 0


@decor_path(r'C:\Users\rudol\Desktop\decorator\log.txt')
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
                result = search(word, text)
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
                result = search(word, text)
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












