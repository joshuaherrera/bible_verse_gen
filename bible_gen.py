#!/usr/bin/env python3
# 01/04/2019 initial version


import requests
# import json
from config import credentials


def bible_gen():
    # Note, this url will return all bible translations available
    url = "https://api.scripture.api.bible/v1/bibles"
    headers = {'api-key': credentials['key']}
    res = requests.get(url, headers=headers)
    print(res.json())


def main():
    bible_gen()


if __name__ == '__main__':
    main()
