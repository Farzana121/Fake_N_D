from bs4 import BeautifulSoup
from Parser.scrapper import Scrapper
from dateutil.parser import parse
import json
import re

# url = 'https://www.prothomalo.com/bangladesh/article/1623496'
# url = 'https://en.prothomalo.com/sports/news/204652/WIndies-get-one-day-series-win-in-five-years'
# url = 'https://www.prothomalo.com/bangladesh/article/1623509/%E0%A6%A8%E0%A6%BF%E0%A6%B7%E0%A7%87%E0%A6%A7%E0%A6%BE%E0%A6%9C%E0%A7%8D%E0%A6%9E%E0%A6%BE-%E0%A6%85%E0%A6%AE%E0%A6%BE%E0%A6%A8%E0%A7%8D%E0%A6%AF-%E0%A6%95%E0%A6%B0%E0%A7%87-%E0%A6%A6%E0%A7%8C%E0%A6%B2%E0%A6%A4%E0%A6%A6%E0%A6%BF%E0%A7%9F%E0%A6%BE-%E0%A6%AA%E0%A6%BE%E0%A6%9F%E0%A7%81%E0%A6%B0%E0%A6%BF%E0%A7%9F%E0%A6%BE-%E0%A6%A8%E0%A7%8C%E0%A6%AA%E0%A6%A5%E0%A7%87'

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

# news = Prothomalo('https://www.prothomalo.com/bangladesh/article/1623496').get_news_dict()
# news = Prothomalo('https://www.prothomalo.com/bangladesh/article/1623496').get_news_json()
# print(news)
