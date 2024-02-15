import requests
from bs4 import BeautifulSoup
from datetime import datetime

from dateutil import parser


def aljazeera_spider(past_urls, worksheets):
        response = requests.get('https://www.aljazeera.com/tag/lgbtq')
        soup = BeautifulSoup(response.content, 'html.parser')
        news_elements = soup.find_all(attrs={'class':"u-clickable-card__link"})
        urls = [e.get("href") for e in news_elements]
        urls = ['https://www.aljazeera.com' + u for u in urls]
        articles_data = []
        for url in urls:
            if url in past_urls:
                continue
            elif url is not None:
                response_2 = requests.get(url)
                soup = BeautifulSoup(response_2.content, 'html.parser')
                title = soup.select('h1')[0].text.strip()
                tag = soup.find(class_="topics").findAll('a')[1].text.strip()
                tags = tag
                raw_date_text = soup.find(
	                'div', {'class': 'date-simple css-1yjq2zp'}).find(
	                'span', {'class': "screen-reader-text"}).text
                raw_date_text = raw_date_text.split('Published On ')[-1]

                date = parser.parse(raw_date_text)
                dt_string = date.strftime('%Y%m%d%H%M')
                p_body = soup.find(attrs={'class':"wysiwyg wysiwyg--all-content css-ibbk12"})
                paragraphs = [tt.text for tt in p_body.find_all('p')]
                content = '\n'.join(paragraphs)
                article_data = {'url': url, 'tags': tags, 'article_source':'aljazeera',
                                'title': title,
                                # 'author': 'ASSOCIATED PRESS',
                                'content': content,
                                'timestamp': dt_string}

                articles_data.append(article_data)
                past_urls.append(url)

        for d in articles_data:
            print(d.keys())

            worksheets.append_table(list(d.values()))
        return True
