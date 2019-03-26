# Bible verse generator

This is a CLI program for returning a verse from the Bible.   
Currently returns a random verse from the King James Version of the Bible.   
Uses the American Bible Society's [API.Bible](https://scripture.api.bible/).   

### Usage   
<!-- good example of readme for options: https://raw.githubusercontent.com/Ganapati/RsaCtfTool/master/README.md -->
```
usage: ./bible_gen.py
```   
Requires the use of an API key from [API.Bible](https://scripture.api.bible/), stored in a seperate file called config.py. This file should contain a dictionary in the form of {"key": GENERATED_KEY}.  