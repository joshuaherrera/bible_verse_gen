#!/usr/bin/env python3
# 01/04/2019 initial version


import random
from html.parser import HTMLParser
import requests
import requests_cache
from config import credentials

requests_cache.install_cache('bible_cache', backend='sqlite', expire_after=24*60*60)

class MLStripper(HTMLParser):
    '''
    HTML parser child class of html parser that is used to strip html
    content from data. Used to strip content from returned verses
    '''
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def query_bible_api(url, headers, parameters=None):
    '''
    Queries api to get json data. expects a dictionary as the
    parameters. if none supplied, just return all bibles.
    '''
    if parameters:
        res = requests.get(url, headers=headers, params=parameters)
    else:
        res = requests.get(url, headers=headers)
    # print(res.from_cache) # checks if response is from cache
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
    verses = ['GEN.1.1', 'JAS.1.17', 'ROM.8.28', 'JER.29.11', 'JHN.3.16-17',
              'EPH.6.12', 'HEB.11.6', 'JAS.1.19', 'JAS.1.22', 'JAS.3.18',
              'JAS.5.7', 'REV.19.16', 'REV.21.4', 'REV.22.13', 'ROM.6.23',
              'ROM.8.31', 'ROM.8.38-39', 'JHN.1.12', 'MAT.6.25', 'MAT.24.27',
              'MAT.28.19', 'MRK.8.34', 'MRK.10.27', 'MRK.11.26', 'LUK.12.8',
              'LUK.18.27', 'ROM.1.16', 'ROM.3.10', 'ROM.3.23', 'ROM.4.8',
              'ROM.5.18', 'ROM.10.9', 'ROM.12.2', 'ROM.12.9', 'ROM.12.12',
              '2CO.2.14-16', '2CO.4.18', '2CO.5.21', '2CO.10.3-6',
              'EPH.6.11-13', 'PHP.1.21', 'PHP.4.13', 'PHP.4.19', 'COL.3.17',
              '2TH.3.16', '2TH.2.15', '1TI.2.5', '2TI.2.10', '2TI.2.15',
              '2TI.2.22', 'HEB.11.3', '2PE.3.9', '1JN.2.15-17', 'PSA.73.26',
              'PRO.10.27', 'PRO.17.27-28', 'PRO.1.7', 'PRO.26.11', 'GEN.50.20',
              'JOS.24.14-15', 'ISA.40.30-31', 'MAT.9.11-12', '1CO.10.13',
              'HEB.13.2', '1PE.4.8', 'LUK.6.31', '1CO.13.4-8', 'LUK.6.32-36']
    # verses = ['PSA.26.14']
    return(random.choice(verses))


def build_params(verse):
    '''
    This function builds the parameters requests will use to query the
    API for a verse. Returns a dictionary with the parameters for generating
    a verse. Generated from https://scripture.api.bible/livedocs
    '''
    parameters = {'query': verse}
    return parameters


# TODO: Find NoneType Error.
#       cache entire bible
#       search cached bible
#       bible selection from language.
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
    # verse_id = 'JHN.3.16-17' # testing for cache usage
    # print(verse_id)
    url = start_url + '/' + bible_id + '/search'
    parameters = build_params(verse_id)
    res_data = query_bible_api(url, headers, parameters)
    # print(res_data)
    book_chapter = res_data['passages'][0]['reference']
    stripped = strip_tags(res_data['passages'][0]['content'])
    verse = ''.join([i for i in stripped if not i.isdigit()])  # remove digits
    print(book_chapter + '\n\t' + verse)


def main():
    bible_verse_gen()


if __name__ == '__main__':
    main()
