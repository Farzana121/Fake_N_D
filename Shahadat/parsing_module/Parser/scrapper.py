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
