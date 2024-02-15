import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import parser

import re


def guardian_spider(past_urls=[], worksheets=None):
        response = requests.get('https://www.theguardian.com/world/lgbt-rights')
        soup = BeautifulSoup(response.content, 'html.parser')
        news_elements = [ele.find_all(attrs={'class': "fc-item__link"})[0] for ele in soup.find_all(attrs={'class':"fc-item__title"})]
        urls = [e.get("href") for e in news_elements]

        articles_data = []
        for url in urls:
            if url in past_urls:
                continue
            elif url is not None:
                print(url)
                response_2 = requests.get(url)
                soup = BeautifulSoup(response_2.content, 'html.parser')
                title = soup.select('h1')[0].text.strip()

                tags = [ele.find_all('a')[0].text for ele in  soup.find_all(attrs={'class': "dcr-pagas8"})]
                tags = ', '.join(tags)

                date_text_ele = [ele.text for ele in soup.find_all('span', {'class': "dcr-u0h1qy"})]
                dt_string = ''
                if date_text_ele:
                    date_text_ele = ' '.join(date_text_ele[0].split(' ')[1:-1])
                    # datetime.strftime('')
                    dt_string = datetime.strptime(date_text_ele, "%d %b %Y %H.%M")
                else:
                    date_text_ele = [ele.text for ele in soup.find_all('div', {'class': "dcr-1d52k2r"})]

                    if date_text_ele:
                        date_text_ele = ' '.join(date_text_ele[0].split(' ')[1:-1])
                        # datetime.strftime('')
                        dt_string = datetime.strptime(date_text_ele, "%d %b %Y %H.%M")
                    else:
                        continue
                dt_string = dt_string.strftime('%Y%m%d%H%M')
                paragraphs = [ele.text for ele in soup.find_all('p', {'class': re.compile('dcr-.*')})]
                content = '\n'.join(paragraphs)
                author_eles = soup.find_all('a', {'rel': 'author'})
                author_ele = None
                if not author_eles:
                    author_eles_lala = soup.find_all( {'class': 'dcr-2py16t'})
                    if author_eles_lala:
                        author_ele = author_eles_lala[0].find_all('span')[0].text
                else:
                    author_ele = author_eles[0]
                if author_ele is not None:

                    author = author_ele.text
                else:
                    author = ''
        #       past_urls.append(url)

                article_data = {'url': url, 'tags': tags, 'article_source': 'guardian',
                                'title': title,
                                'author': author,
                                'content': content,
                                'timestamp': dt_string}
                articles_data.append(article_data)
        for d in articles_data:
            print(d)
            worksheets.append_table(list(d.values()))
        return True
