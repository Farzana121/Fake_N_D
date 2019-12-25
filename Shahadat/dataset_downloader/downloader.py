from .util import create_dir, is_folder_exists
import random
import json

dataset_dir = 'data_set'


def store_news(news, save_dir, valid):
    name = ''.join(random.choice("012345") for i in range(7))
    create_dir("{}/{}".format(save_dir, valid))
    if news:
        # json.dump(news,
        #           open("{}/{}/{}.json".format(save_dir, valid, name), "w"))
        with open("{}/{}/{}.json".format(save_dir, valid, name), 'w', encoding='utf-8') as f:
            f.write(news)


def dowload_dataset(item_list, news_source):
    create_dir('{}/{}'.format(dataset_dir, news_source))
    save_dir = '{}/{}'.format(dataset_dir, news_source)
    for item in item_list:
        url = item.link
        valid = item.valid
        news_json = Prothomalo(url).get_news_json()
        store_news(news_json, save_dir, valid)
