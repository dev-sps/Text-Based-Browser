import os
import sys
import requests
from _collections import deque
from bs4 import BeautifulSoup
from colorama import init, Fore

init(autoreset=True)
history = deque()
args = sys.argv
dir_name = args[1]  # stores the directory name
searchable_tags = ('p', 'a')

# create a directory with dir_name
if not os.path.exists(dir_name):
    os.mkdir(dir_name)


def get_url(in_url):
    """
    convert url into proper url
    :param in_url:
    :return: url with https
    """
    if input_url.startswith("https"):
        return in_url
    in_url = "https://" + in_url
    return in_url


def get_text(ur):
    """
    get the text of the requested website
    :param ur:
    :return: website text
    """
    r = requests.get(ur)
    return r.text


def get_file_name(url):
    """
    extract file name from the url
    :param url:
    :return:
    """
    if url.startswith("https"):
        # ignore first 8 characters https://
        res = url[8:].split(".", 1)
    else:
        res = url.split(".", 1)
    return res[0]


def mk_file(text, url_1):
    """
    :param text:
    :param url_1:
    :return:
    """
    url_1 = get_file_name(url)
    with open(f'{dir_name}/{url_1}', 'w+') as file:
        soup = BeautifulSoup(text, 'lxml')
        for link in soup.find_all(searchable_tags):
            if link.find('a'):
                file.writelines(Fore.BLUE + link.get_text())
                print(Fore.BLUE + link.get_text())
            else:
                file.writelines(link.get_text() + '\n')
                print(link.get_text() + '\n')
    history.append(url_1)


def read_file(file_name):
    with open(f'{dir_name}/{file_name}', 'r') as read:
        for k in read:
            print(k)


def check_input_url(a):
    if "." in a:
        return True
    return False


def back():
    history.pop()
    k = history.pop()
    read_file(k)
    history.append(k)


while True:
    input_url = input("entry: ")

    if input_url == 'exit':
        break

    elif input_url == 'back':
        if len(history) <= 1:
            continue
        else:
            back()

    elif input_url in history:
        read_file(input_url)

    elif check_input_url(input_url) == 0:
        print("Error: Incorrect Url")

    else:
        url = get_url(input_url)
        result = get_text(url)
        mk_file(result, url)
