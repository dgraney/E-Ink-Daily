import os
import requests
import datetime
import json

class WeatherData():
    dailyWeather = []

class DailyWeatherData():
    LowTemp = None
    HighTemp = None
    Description = None
    Icon = None
    TimeStamp = None


def getDarkApiKey():
    with open('darkSky.key') as keyFile:
        key = keyFile.readline()
    return key
    
def getLatLong():
    with open('latlong.loc') as latLongFile:
        latLong = latLongFile.readline()
    lat,lon = latLong.split(',')
    print(lat)
    print(lon)
    return lat,lon

def getWeatherByLatLong(darkApiKey,lat,lon):
    URL  = 'https://api.darksky.net/forecast/%s/%s,%s' % (darkApiKey,lat,lon)
    r = requests.get(url=URL)
    data = r.json()
    return data

def extractWeatherData(data):
    longDailyData = data['daily']
    dailyData = longDailyData['data']
    weatherData = WeatherData()
    for dayData in dailyData:
        dailyWeatherData = DailyWeatherData()
        dailyWeatherData.LowTemp = dayData['temperatureLow']
        dailyWeatherData.HighTemp = dayData['temperatureHigh']
        dailyWeatherData.Description = dayData['summary']
        dailyWeatherData.Icon = dayData['icon']
        dailyWeatherData.TimeStamp = dayData['time']
        
        weatherData.dailyWeather.append(dailyWeatherData)

    return weatherData

def main():
    key = getDarkApiKey()
    lat,lon = getLatLong()
    data = getWeatherByLatLong(key,lat,lon)
    weatherData = extractWeatherData(data)
    for daily in weatherData.dailyWeather:
        ts = int(daily.TimeStamp)
        weekDay = datetime.date.fromtimestamp(ts).strftime('%a')
        print(weekDay)
        print("    Daily Description: %s" % daily.Description)
        print("    Daily High/Low: %s/%s" % (daily.HighTemp,daily.LowTemp))
    return weatherData

if __name__ == "__main__":
    key = getDarkApiKey()
    lat,lon = getLatLong()
    data = getWeatherByLatLong(key,lat,lon)
    weatherData = extractWeatherData(data)
    for daily in weatherData.dailyWeather:
        ts = int(daily.TimeStamp)
        weekDay = datetime.date.fromtimestamp(ts).strftime('%a')
        print(weekDay)
        print("    Daily Description: %s" % daily.Description)
        print("    Daily High/Low: %s/%s" % (daily.HighTemp,daily.LowTemp))

