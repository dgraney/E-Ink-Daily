import sys
sys.path.insert(0, './scripts')
sys.path.insert(0, './epaper')
#import quickStart as calendar
import dailyVerse as dailyVerse
import weather as weather

import epd7in5 as epd7in5
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import datetime

class ProjectDaily():
    def __init__ (self):
        self.dailyBibleVerse = dailyVerse.getDailyVerse()
        self.weatherData = weather.main()
        #self.calendarEvents = calendar.main()
        
        self.iconDict = {
            "clear-day": "B",
            "clear-night": "C",
            "rain": "R",
            "snow": "U",
            "sleet": "W",
            "wind": "S",
            "fog": "L",
            "cloudy": "N",
            "partly-cloudy-day": "H",
            "partly-cloudy-night": "I",
            "thunderstorm":"O" ,
            "hail": "X",
        }

        
        global font65; font65= ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 65)
        global font48; font48 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 48)
        global font36; font36 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 36)
        global font24; font24 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 24)
        global font18; font18 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 18)
        global weather_icons; weather_icons = ImageFont.truetype('./fonts/meteocons-webfont.ttf', 100)
        #self.drawData()

    def drawData(self):
        try:
            epd = epd7in5.EPD()
            epd.init()
            print("Clear")
            epd.Clear(0xFF)

            print("Drawing")
            self.W = epd7in5.EPD_WIDTH
            self.H = epd7in5.EPD_HEIGHT
            Limage = Image.new("1",( self.H,self.W ),255)
            draw = ImageDraw.Draw(Limage)
            
            # weatherData = 
            todayWeatherData = self.weatherData.dailyWeather[0]
            ts = int(todayWeatherData.TimeStamp)
            weekDay = datetime.date.fromtimestamp(ts).strftime('%A')
            date = datetime.date.fromtimestamp(ts).strftime('%m/%d/%Y')
            todayIconAsText = todayWeatherData.Icon
            todayIconString = self.iconDict[todayIconAsText]
            todayHighLowWeather = str(todayWeatherData.HighTemp) + " / " + str(todayWeatherData.LowTemp)


            self.drawCenteredText(draw,weekDay,font65,0)
            self.drawCenteredText(draw,date,font48,75)
            self.drawCenteredText(draw,todayIconString,weather_icons,110)
            self.drawCenteredText(draw,todayHighLowWeather,font24,200)

            epd.display(epd.getbuffer(Limage))
            time.sleep(2)
            epd.sleep()
        except:
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            exit()

    def drawCenteredText(self,draw,value,font,height):
        w,h = draw.textsize(value,font = font)
        weatherCtr = (((self.H-w)/2,height))
        draw.text(weatherCtr,value,font = font,fill = 0)

if __name__ == "__main__":
    projDaily = ProjectDaily()
    projDaily.drawData()