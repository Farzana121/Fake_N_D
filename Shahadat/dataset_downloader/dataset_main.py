import pandas as pd
from Scrapper.dataset_downloader.util import Item, create_dir
from Scrapper.dataset_downloader.downloader import dowload_dataset
from Scrapper.dataset_downloader.fb_scrapper import FBScrapper
from Scrapper.dataset_downloader.news_content_collection import NewsContentCollector
import csv
import time

base_path = "./data/"


def store_source_link(title, real, fake):
    with open("{}/{}_real.csv".format(base_path, title), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Link", "Title", "Valid"])
        for item in real:
            writer.writerow([item.link, item.title, item.valid])
    with open("{}/{}_fake.csv".format(base_path, title), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Link", "Title", "Valid"])
        for item in fake:
            writer.writerow([item.link, item.title, item.valid])


def parse_news_source_list(title, path):
    df = pd.read_csv(path, encoding='utf-8')
    real = list()
    fake = list()

    for index, row in df.iterrows():
        print(row['Link'])
        news_link = FBScrapper(row['Link']).get_news_url()
        print("newslink:", news_link)
        if news_link is None:
            continue
        item = Item(news_link, row["Title"], row['Valid'])
        if item.valid == 'agree':
            real.append(item)
        else:
            fake.append(item)

    store_source_link(title, real, fake)


def make_source_list(path):
    df = pd.read_csv(path, encoding='utf-8')
    real = list()
    fake = list()
    # print(df)
    for index, row in df.iterrows():
        item = Item(row["Link"], row["Title"], row['Valid'])
        real.append(item)
    return real


if __name__ == "__main__":
    # source_link = base_path + "news_source.csv"
    # parse_news_source_list("source", source_link)
    # real = make_source_list(base_path + "source_fake.csv")
    # real = make_source_list(base_path + "source_real.csv")
    real = make_source_list(base_path + "twitter_fake.csv")
    NewsContentCollector(real, 'fake').collect_data()
