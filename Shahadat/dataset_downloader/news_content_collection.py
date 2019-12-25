import json
import logging
import time

import requests
from tqdm import tqdm
from newspaper import Article
from .util import create_dir
import random
import csv
from urllib.parse import urlparse
from Scrapper.dataset_downloader.prothomalo import Prothomalo

base_path = "./dataset/"

def get_epoch_time(time_obj):
    if time_obj:
        return time_obj.timestamp()

    return None


def crawl_link_article(id_type, url):
    name = ''.join(random.choice("012345") for i in range(7))
    id = id_type + "_" + name
    url = url.strip()

    url_parse_result = urlparse(url)
    base_url = url_parse_result.netloc


    result_json = None

    try:
        if 'http' not in url:
            if url[0] == '/':
                url = url[1:]
            try:
                article = Article('http://' + url)
                article.download()
                time.sleep(2)
                article.parse()
                flag = True
            except:
                logging.exception("Exception in getting data from url {}".format(url))
                flag = False
                pass
            if flag == False:
                try:
                    article = Article('https://' + url)
                    article.download()
                    time.sleep(2)
                    article.parse()
                    flag = True
                except:
                    logging.exception("Exception in getting data from url {}".format(url))
                    flag = False
                    pass
            if flag == False:
                return None
        else:
            try:
                article = Article(url)
                article.download()
                time.sleep(2)
                article.parse()
            except:
                logging.exception("Exception in getting data from url {}".format(url))
                return None

        if not article.is_parsed:
            return None

        visible_text = article.text
        top_image = article.top_image
        images = article.images
        keywords = article.keywords
        authors = article.authors
        canonical_link = article.canonical_link
        title = article.title
        meta_data = article.meta_data
        movies = article.movies
        publish_date = article.publish_date
        source = article.source_url
        summary = article.summary
        text = meta_data['description']

        if base_url == 'www.prothomalo.com':
            prothomalo = Prothomalo(url).get_news_dict()
            if prothomalo['body'] != "":
                text = prothomalo['body']
            else:
                text = meta_data['description']

        result_json = {'url': url, 'text': visible_text, 'images': list(images), 'top_img': top_image,
                       'keywords': keywords,
                       'authors': authors, 'canonical_link': canonical_link, 'title': title, 'meta_data': meta_data,
                       'movies': movies, 'publish_date': get_epoch_time(publish_date), 'source': source,
                       'summary': summary}
    except:
        logging.exception("Exception in fetching article form URL : {}".format(url))

    return [id, title, text, url, top_image, authors, source, get_epoch_time(publish_date), movies, images,
            canonical_link, meta_data]


#     return meta_data['description']

def collect_news_articles(news_list, label):
    # for source in news_list:
    #     news_article = crawl_link_article(source.link)
    with open("{}/dataset_{}.csv".format(base_path, label), 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        t = 0
        writer.writerow(["id", "title", "text", "url", "top_image", "authors", "source","publish_date", "movies", "images","canonical_link", "meta_data"])
        for source in news_list:
            t+=1
            if t%50==0:
                time.sleep(30)
            x = crawl_link_article(label,source.link)
            while x is None:
                x = crawl_link_article(label, source.link)
            writer.writerow(x)
            print(t, " : ok")


class NewsContentCollector:
    def __init__(self, news_list, label):
        self.news_list = news_list
        self.label = label
        create_dir(base_path)

    def collect_data(self):
        collect_news_articles(self.news_list, self.label)


class SingleNewsCollector:
    def collect_single_news(self, url):
        news_data = crawl_link_article("", url)
        return (news_data[1], news_data[2])
