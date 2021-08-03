import string

import requests

from bs4 import BeautifulSoup

import os

number_of_pages = int(input())
type_of_articles = input()
absolute_path = os.getcwd()

for i_ in range(number_of_pages):
    r = requests.get(f"https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page={i_+1}")
    articles = BeautifulSoup(r.content, "html.parser").find_all('article')
    os.chdir(absolute_path)
    os.mkdir(f'Page_{i_+1}')
    os.chdir(f'Page_{i_+1}')

    for link in articles:
        if link.find_all('span')[-1].text == type_of_articles:
            title = str(link.find('a').text).translate(str.maketrans('', '', string.punctuation)).replace(' ', '_')
            file = open(f'{title}.txt', 'w', encoding='utf-8')

            link = "https://www.nature.com" + link.find('a')['href']

            article = BeautifulSoup(requests.get(link).text, 'html.parser')
            if article.find('div', {'class': 'article-item__body'}):
                file.write(article.find('div', {'class': 'article-item__body'}).text.strip())
            elif article.find('div', {'class': 'c-article-body u-clearfix'}):
                file.write(article.find('div', {'class': 'c-article-body u-clearfix'}).text.strip())

            file.close()

print('Saved all articles.')
