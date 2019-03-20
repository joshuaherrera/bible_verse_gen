#!/usr/bin/env python3
# 01/04/2019 initial version


import random
import requests
from config import credentials


def query_bible_api(url, headers, parameters=None):
    '''
    Queries api to get json data. expects a dictionary as the
    parameters. if none supplied, just return all bibles.
    '''
    if parameters:
        res = requests.get(url, headers=headers, params=parameters)
    else:
        res = requests.get(url, headers=headers)
    return res.json()['data']


def get_langs(data):
    '''
    Takes as input a dictionary of data from the API. Builds up a dictionary
    of the available languages from the returned query. Ensures duplicate
    languages are not stored in the dictionary by checking if an input is
    already in the data structure.
    '''
    languages = {}
    for i in data:
        iso639_lang = i['language']['id']
        lang_name = i['language']['name']
        if lang_name not in languages:
            languages[lang_name.lower()] = iso639_lang
    return languages


def display_langs(languages):
    '''
    Displays the available languages to choose from. Receives as input a
    dictionary of available languages. Returns nothing.
    '''
    for i, j in languages.items():
        print(j, i.capitalize())


def set_lang(languages):
    '''
    Queries user for language input to query the API. Detects if ISO639
    abbreviation is given or a full language name is given.
    Exptects as input a dictionary containing the available languages to
    choose from. Returns a string containing the selected language.
    '''
    while True:
        lang_selection = input("Select a language using the ISO639 code or full language name: ")
        lang_selection = lang_selection.lower()
        if len(lang_selection) == 3 and lang_selection in languages.values():
            return lang_selection
        # searches the keys in the dict
        elif lang_selection in languages:
            return languages[lang_selection]
        else:
            print("Invalid selection.")


def get_bible_version(data):
    '''
    uses data (type list) to get the name, abbreviation, and unique
    id's of the available bible translations for a chosen language.
    returns a dict with the name as the key, and a list, containing
    the abbreviation and unique id, as the corresponding value.
    '''
    versions = {}
    for i in data:
        vers_id = i['id']
        vers_name = i['name']
        vers_abbrev = i['abbreviation']
        vers_list = [vers_id, vers_name]
        if vers_abbrev not in versions:
            versions[vers_abbrev.lower()] = vers_list
    return versions


def get_random_verse():
    '''
    This function returns a random verse ID from a list of preselected verses.
    Returns a string containing the verse ID.
    '''
    verses = ['GEN.1.1', 'JAS.1.17', 'ROM.8.28']
    # verses = ['JAS.1.17', 'ROM.8.28']
    return(random.choice(verses))


def build_params():
    '''
    This function builds the parameters requests will use to query the
    API for a verse. Returns a dictionary with the parameters for generating
    a verse. Generated from https://scripture.api.bible/livedocs
    '''
    parameters = {'content-type': 'text',
                  'include-notes': 'false', 'include-titles': 'true',
                  'include-chapter-numbers': 'false',
                  'include-verse-numbers': 'false',
                  'include-verse-spans': 'false'}
    return parameters


# TODO: bible selection from language.
#       Decide whether to set language using --options.
#       Decide whether to display available bibles or use a
#       default for a language.
#       Group verses by topic.
#       Select random verse by topic.
#       Display all verses by topic.


def bible_verse_gen():
    '''
    This function will query the Bible API and print a random verse.
    '''
    # Note, this url will return all bible translations available
    start_url = "https://api.scripture.api.bible/v1/bibles"
    headers = {'api-key': credentials['key']}
    bible_id = 'de4e12af7f28f599-01'  # use KJV as default
    verse_id = get_random_verse()
    url = start_url + '/' + bible_id + '/verses/' + verse_id
    parameters = build_params()
    res_data = query_bible_api(url, headers, parameters)
    # print(res_data)
    book_chapter = res_data['reference']
    verse = res_data['content'].rstrip()
    print(book_chapter + '\n' + verse)


def main():
    bible_verse_gen()


if __name__ == '__main__':
    main()
