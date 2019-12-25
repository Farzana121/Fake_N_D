from Scrapper.scrapper import Scrapper
from bs4 import BeautifulSoup, Comment
from urllib.parse import unquote
import re

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class FBScrapper:
    def __init__(self, url):
        self.url = url
        scrapper = Scrapper(self.url)
        raw_data = scrapper.scrape_site()
        self.soup = BeautifulSoup(raw_data.text, "html.parser")

    def get_news_url(self):
        """Parsing the news url from fb link"""
        try:
            comments = self.soup.find_all(string=lambda text: isinstance(text, Comment))
            #         print(comments)
            sources = ["prothomalo.com", "jugantor.com", "ittefaq.com"]
            target = ""
            commented_a = []
            for source in sources:
                x = list(filter(lambda i: source in str(i), comments))
                if len(x) > 0:
                    commented_a = x
                    target = source
                    break
                    #         print(commented_a)
                    #         print(target)
            a = BeautifulSoup(commented_a[0], "html.parser")
            #         print(a)
            all_links = [a['href'] for a in a.find_all('a', href=True)]
            #         print(all_links)

            # Find valid link
            valid_link = list(filter(lambda i: target in str(i), all_links))
            # print(valid_link[0])

            # Unquoted the valid link
            url = unquote(valid_link[0])
            # print(url)

            prothom_alo = \
            re.findall('=http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)[0]
            # print(prothom_alo)

            prothom_alo = prothom_alo[1:]
            print(prothom_alo)
            return prothom_alo
        except:
            return None


# url = "https://www.facebook.com/dainikIttefaq/posts/2342110555898770?__tn__=-R"
# news = FBScrapper(url).get_news_url()
# print(news)