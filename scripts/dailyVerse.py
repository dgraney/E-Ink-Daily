import os
import requests
import datetime
import json

def getDailyVerse():
    url = 'http://labs.bible.org/api/?passage=votd&type=json'
    r = requests.get(url)
    return r.json()[0]

if __name__ == "__main__":
    getDailyVerse()