import csv
import os
import re
import errno


def extract_text_from_tag(txt):
    """This function will extract string from a tag"""
    text = str(txt)
    clean = re.compile('<.*?>')
    cleaned_text = (re.sub(clean, '', text))
    return cleaned_text


class Item:
    """This data holder for CSV new item"""

    def __init__(self, link, title, valid):
        self.link = link
        self.title = title
        self.valid = valid


def create_dir(dir_name):
    """Create directory if folder not exist"""
    if not os.path.exists(dir_name):
        try:
            os.makedirs(dir_name)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def is_folder_exists(folder_name):
    """Check if the folder exist or not"""
    return os.path.exists(folder_name)
