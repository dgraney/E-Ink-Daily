import os
import requests
import datetime
import json

def getDailyVerse():
    url = 'http://labs.bible.org/api/?passage=votd&type=json'
    r = requests.get(url)
    dailyVerseJson = r.json()[0]
    verseText = "%s %s:%s" % (dailyVerseJson['bookname'],dailyVerseJson['chapter'],dailyVerseJson['verse'])

    verse = getVerse(verseText)
    return verse

def getVerse(verseRange):
    url = 'https://bible-api.com/%s?translation=kjv' % verseRange
    r = requests.get(url)
    print(r.json())
    return r.json()
if __name__ == "__main__":
    getDailyVerse()
