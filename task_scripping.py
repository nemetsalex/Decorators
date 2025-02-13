# код приложения из д/з по скрапингу с примененным декоратором 

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
from main3 import log_decorator


@log_decorator('articles.json')
def write_article(path, art_list):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(art_list, f, ensure_ascii=False, indent=4)


KEYWORDS = ['дизайн', 'фото', 'web', 'python']
url = 'https://habr.com/ru/articles/'
headers = {'User-Agent': 'Mozilla/5.0'}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f'Ошибка запроса: {e}')
    exit()

soup = BeautifulSoup(response.text, 'lxml')
articles = soup.find_all('article')

articles_list = []

for article in articles:
    title_tag = article.find('h2').find('a') if article.find('h2') else None
    if not title_tag:
        continue
    
    title = title_tag.text.strip()
    link = f'https://habr.com{title_tag["href"]}'
    
    time_tag = article.find('time')
    date = time_tag.get('datetime', 'Неизвестно') if time_tag else 'Неизвестно'
    
    if date != 'Неизвестно':
        date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M')

    preview = article.select_one('.article-formatted-body')
    preview_text = preview.text.strip().lower() if preview else ''

    if any(keyword.lower() in preview_text for keyword in KEYWORDS):
        print(f'{date} – {title} – {link}')
        articles_list.append({'date': date, 'title': title, 'link': link})

if articles_list:
    write_article('articles.json', articles_list)
    # with open('articles.json', 'w', encoding='utf-8') as f:
    #     json.dump(articles_list, f, ensure_ascii=False, indent=4)