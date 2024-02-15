import pygsheets
import pandas as pd

from advocate import advocate_spider
from ap_news import ap_spider
from aljazeera import aljazeera_spider
from guardian import guardian_spider

def get_sheet_info(config, google_spreadsheet):
    gc = pygsheets.authorize(service_file=config)
    # provide the json_file name including the .json extension
    google_spreadsheet = gc.open_by_url(google_spreadsheet)
    #provide the url of the g-sheet.
    worksheets = google_spreadsheet.worksheet(
        property="title",value="articles_info")

    articles_records = pd.DataFrame(worksheets.get_all_records())
    try:
        past_urls = list(articles_records['url'].values)
    except KeyError:
        past_urls = []
    return worksheets, past_urls


def spider(worksheets, past_urls):

    # res_ap = ap_spider(past_urls, worksheets)
    res_advoc = advocate_spider(past_urls, worksheets)

    res_news = ap_spider(past_urls, worksheets)

    res_aljazeera = aljazeera_spider(past_urls, worksheets)

    res_guardian = guardian_spider(past_urls, worksheets)

    return res_advoc, res_news, res_aljazeera, res_guardian


def spider_dev(worksheets, past_urls):

    # res_ap = ap_spider(past_urls, worksheets)
    res_advoc = advocate_spider(past_urls, worksheets)

    res_news = ap_spider(past_urls, worksheets)

    res_aljazeera = aljazeera_spider(past_urls, worksheets)

    return res_aljazeera





