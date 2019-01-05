#!/usr/bin/env python3
# 01/04/2019 initial version


import requests
# import json
from config import credentials


def get_langs(data):
    # uses initial query to store available languages in a dict
    # checks if a key exists, if so skips that iteration to store
    # only unique keys and values.
    languages = {}
    for i in data:
        iso639_lang = i['language']['id']
        lang_name = i['language']['name']
        if lang_name not in languages:
            languages[lang_name.lower()] = iso639_lang
    return languages


def display_langs(languages):
    # displays available languages
    for i, j in languages.items():
        print(j, i.capitalize())


def set_lang(languages):
    # queries the user for a language selection and returns it.
    while True:
        lang_selection = input("Select a language using the ISO639 code or full language name: ")
        lang_selection = lang_selection.lower()
        if len(lang_selection) == 3 and lang_selection in languages.values():
            return lang_selection
        elif lang_selection in languages:
            return languages[lang_selection]
        else:
            print("Invalid selection.")


def query_bible_vers(url, headers, lang):
    # queries api to get json data for a language
    parameters = {'language': lang}
    res = requests.get(url, headers=headers, params=parameters)
    return res.json()['data']


def get_bible_vers(data):
    # uses data (type list) to get the name, abbreviation, and unique
    # id's of the available bible translations for a chosen language.
    # returns a dict with the name as the key, and a list, containing
    # the abbreviation and unique id, as the corresponding value.
    pass


def bible_verse_gen():
    # Note, this url will return all bible translations available
    url = "https://api.scripture.api.bible/v1/bibles"
    headers = {'api-key': credentials['key']}
    res = requests.get(url, headers=headers)
    res_data = res.json()['data']
    languages = get_langs(res_data)
    display_langs(languages)
    chosen_lang = set_lang(languages)
    print(chosen_lang)
    # parameters = {'language': chosen_lang}
    # res = requests.get(url, headers=headers, params=parameters)
    # print(res.json())


def main():
    bible_verse_gen()


if __name__ == '__main__':
    main()
