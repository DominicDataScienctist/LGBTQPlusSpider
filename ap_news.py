import requests
from bs4 import BeautifulSoup
from datetime import datetime


def ap_spider(past_urls, worksheets):
        response = requests.get('https://apnews.com/hub/lgbtq-people')
        soup = BeautifulSoup(response.content, 'html.parser')
        news_elements = soup.find_all(attrs={'class':"Link"})
        urls = [e.get("href") for e in news_elements]
        articles_data = []
        for url in urls:
            if url in past_urls:
                continue
            elif url is not None and 'article' in url:
                response_2 = requests.get(url)
                soup = BeautifulSoup(response_2.content, 'html.parser')
                title = soup.select('h1.Page-headline')[0].text.strip()
                tags = soup.find_all(attrs={'class':"Page-breadcrumbs"})[0].text
                badges = soup.find_all(attrs={'class':"Page-dateModified"})
                badges_str = str(badges)
                badges_str = badges_str.split('data-timestamp="')[-1]
                badges_str = badges_str.split('"')[0]
                created_on_ts = int(badges_str) / 1000.0
                dt = datetime.utcfromtimestamp(created_on_ts)
                dt_string = dt.strftime('%Y%m%d%H%M')
                p_body = soup.find(attrs={'class':"RichTextStoryBody RichTextBody"})
                paragraphs = [tt.text for tt in p_body.find_all('p')]
                content = '\n'.join(paragraphs)
                article_data = {'url': url, 'tags': tags, 'article_source':'ap_news',
                                'title': title,
                                # 'author': 'ASSOCIATED PRESS',
                                'content': content,
                                'timestamp': dt_string}

                articles_data.append(article_data)
                past_urls.append(url)
        for d in articles_data:
            worksheets.append_table(list(d.values()))
        return True
