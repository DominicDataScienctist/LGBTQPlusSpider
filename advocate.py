import requests
from bs4 import BeautifulSoup
import dateutil

START = "By continuing to use our site, you agree to our Private Policy and Terms of Use."
END = "contributed to this report."


def advocate_spider(past_urls, worksheets):
	# try:
		response = requests.get('https://www.advocate.com/')
		soup = BeautifulSoup(response.content, 'html.parser')

		news_elements = soup.find_all(attrs={'class': 'widget__headline-text custom-post-headline'})
		urls = [e.get("href") for e in news_elements]
		advocate_articles_data = []
		for url in urls:

			if url in past_urls:
				continue
			else:
				response_2 = requests.get(url)
				soup = BeautifulSoup(response_2.content, 'html.parser')
				title = soup.find(attrs={'class': "widget__headline-text custom-post-headline"}).text
				title = title.replace('\n', '')
				title = title.strip()

				paragraphs = []
				started = False
				date_str = soup.find(attrs={'class': "social-date__text"}).text
				dt = dateutil.parser.parse(date_str)
				dt_string = dt.strftime('%Y%m%d%H%M')
				try:
					tags_elements = soup.find(class_="tags").findAll('a')
					tags = [c.text for c in tags_elements]
				except AttributeError:
					tags = []
				tags = ', '.join(tags)
				for p in soup.find_all('p'):
					if START in p.text:
						pass
					else:
						started = True

					if END in p.text:
						last_line = p.text
						last_line = last_line.split("The Advocate's ")[-1]
						author = last_line.split(" contributed to this report")[0]
						content = '\n'.join(paragraphs)
						break

					if started:
						paragraphs.append(p.text)

				paragraphs = [p.text for p in soup.find_all('p') if START not in p.text and END not in p.text]
				paragraph = '\n'.join(paragraphs).strip()

				article_data = {'url': url, 'tags': tags, 'article_source': 'advocate', 'title': title,
				                # 'author': author,
				                'content': paragraph, 'timestamp': dt_string}
				advocate_articles_data.append(article_data)
				past_urls.append(url)

		for d in advocate_articles_data:
			worksheets.append_table(list(d.values()))
		return True
	# except Exception:
	# 	return False