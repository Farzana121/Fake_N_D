import logging
import time
from newspaper import Article
import random
import csv
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from dateutil.parser import parse
import json
import re
import requests

class Scrapper:
    _header = {'Accept-Encoding': 'gzip, deflate, sdch',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/41.0.2272.118 Safari/537.36'}

    def __init__(self, url):
        self._url = url

    def scrape_site(self):
        """Scrape raw data from this url"""
        if self._url is not None:
            res = requests.get(self._url, headers=self._header, verify=False)
            if res.status_code == 200:
                print("status code 200!!!")
                return res
            else:
                print(res.status_code)
                return
        else:
            print("Must give a valid url!")

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
    except:
        logging.exception("Exception in fetching article form URL : {}".format(url))

    return [id, title, text, url, top_image, authors, source, get_epoch_time(publish_date), movies, images,
            canonical_link, meta_data]

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

class Prothomalo:
    def __init__(self, url):
        scrapper = Scrapper(url)
        raw_data = scrapper.scrape_site()
        self.soup = BeautifulSoup(raw_data.text, "html.parser")

    def get_title(self):
        """Parsing the title form news"""
        title = self.soup.title.string
        # title = extract_text_from_tag(soup.find('h1', attrs={'class': 'title'}))  # Title from the body
        # print(soup.title.string)  # Title from the head
        # print(title)
        return title

    def get_category(self):
        """Parsing the category form news"""
        category = self.soup.find('div', attrs={'class': 'breadcrumb'})
        news_category = category.ul.find_all('li').pop().strong.string
        # print(news_category)
        return news_category

    def get_body_images(self):
        """This function will parse the news body and all images"""
        try:
            article = self.soup.find('article')
            article_body = article.find_all('p')
            images = []
            news_body = ''
            clean = re.compile('<.*?>')
            for p in article_body:
                if p.string is None:
                    if p.img is not None:
                        images.append(p.img['src'])
                        if p.img.next_sibling is not None:
                            news_body += p.img.next_sibling
                    else:
                        cleaned_p = re.sub(clean, '', str(p))
                        news_body += cleaned_p

                else:
                    news_body += p.string
                    # news_body += '\n'

            return news_body, images

        except:
            return "", ""

    def get_date(self):
        """This function will parse the news body and all images"""
        date = self.soup.find('span', attrs={"itemprop": "datePublished"})
        date_bn = date.string
        datetime = parse(date['content'])
        return datetime, date_bn

    def get_news_dict(self):
        """This function will generate news dictionary"""
        body, images = self.get_body_images()
        date, date_bn = self.get_date()
        news_dict = {
            'title': self.get_title(),
            'category': self.get_category(),
            'body': body,
            'images': images,
            'date': str(date),
            # 'date_bn': str(date_bn),
        }
        # print(news_dict)
        return news_dict

    def get_news_json(self):
        """This function will return news JSON"""
        news_json = json.dumps(self.get_news_dict()).encode('utf8').decode('unicode-escape')
        return news_json

url = "https://www.prothomalo.com/sports/article/1623715/%E0%A6%AA%E0%A7%81%E0%A6%B0%E0%A7%8B-%E0%A6%AE%E0%A7%8D%E0%A6%AF%E0%A6%BE%E0%A6%9A%E0%A6%87-%E0%A6%96%E0%A7%87%E0%A6%B2%E0%A6%A4%E0%A7%87-%E0%A6%AA%E0%A6%BE%E0%A6%B0%E0%A6%9B%E0%A7%87%E0%A6%A8-%E0%A6%A8%E0%A6%BE-%E0%A6%B0%E0%A7%8B%E0%A6%A8%E0%A6%BE%E0%A6%B2%E0%A6%A6%E0%A7%8B?fbclid=IwAR3U7ebtBdOfAzfeWIVlU8g5P4GLBJzcO-1hjBimMCaoFXJOAEAGhBNXcto&h=AT0O-XBAHP2mgPXhG4c_UT87VR0TCY7NdiJLEFVgNTDKvnnJPRmuTA5AKMGN7lDLFa4s31ZxAk8vd43mhTeF2fnyRRYLy31jTjak00ZU0Wnb6_oeOMltt6z1mjMAc9rwwg8OTVyH2SZUg2cVI0ELxVLcvlp68fgpJYiFM3v7-exD8lEO5mbL_m7Dv-3LdVMTpne4sq6BT8ybgdyBAtMsAYyLpSy49Hxwa65QZnPYs8rFOjXLI--9jMYveWEIHMohatoNRshoDs0EaQBXJLOLNcEE9wkAtO7U6IWSte_7ncYxO7ah_3Nx-eiOkSJacEAOntvmJMmeSqI0yeai5sNYarnRqgM_9qIHOo9dpoK73kiLRPBkFk5jQf59Jw7cu3zhAWlH6dSBZFsjKBmVyxJFt9vOq0CBPHXuG32RVD2P8L0-cFkDl6GaTh6zZ6ceK6IWYCPAd7mnEGoIjYhep4WQfPEGwwVIK4xnQz4Rv3nymVmTM6SgwqMgHIAw3YuNM-shffviPvlUJYtbj0B3sMh55KCZkUu-_knoi_8JcovoFV1z87jAU_pU1UD42aKdR_29wUFCcZvJ1XM3ANgNbpAWQtWyWxOhEEUo7o5L7C3VzVZCJiRcb2LOQC_Au5Hbc5DVjUp-"

news_collector = SingleNewsCollector()
title, body = news_collector.collect_single_news(url)

print(news)
