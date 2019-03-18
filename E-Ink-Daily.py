import sys
sys.path.insert(0, './scripts')
sys.path.insert(0, './epaper')
sys.path.insert(0,'./fonts')
import quickStart as calendar
import dailyVerse as dailyVerse
import weather as weather
from threading import Timer

import epd7in5 as epd7in5
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import datetime
import textwrap

class ProjectDaily():
    def __init__ (self):
        self.dailyBibleVerse = dailyVerse.getDailyVerse()
        self.weatherData = weather.main()
        try:
            self.calendarEvents = calendar.main()
        except:
            self.calendarEvents = None
        
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
        global font20; font20 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 20)
        global font18; font18 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 18)
        global font16; font16 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 16)
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
            """bmp = Image.open("Hershey.bmp")
            epd.display(epd.getbuffer(bmp))"""
            
            # weatherData 
            todayWeatherData = self.weatherData.dailyWeather[0]
            ts = int(todayWeatherData.TimeStamp)
            weekDay = datetime.date.fromtimestamp(ts).strftime('%A')
            date = datetime.date.fromtimestamp(ts).strftime('%m/%d/%Y')
            todayIconAsText = todayWeatherData.Icon
            todayIconString = self.iconDict[todayIconAsText]
            todayHighLowWeather = "H " + str(todayWeatherData.HighTemp) + " | L " + str(todayWeatherData.LowTemp)


            self.drawCenteredText(draw,weekDay,font65,0)
            self.drawCenteredText(draw,date,font48,75)
            self.drawOffsetText(draw,todayIconString,weather_icons,135,offset_frac=0.25)
            self.drawOffsetText(draw,todayHighLowWeather,font24,245,offset_frac=0.25)
            
            draw.rectangle((2,275,self.H-2,330),fill=0)
            self.drawCenteredText(draw,"Upcoming Events",font36,280,_fill=255)
            
            if not self.calendarEvents == None:
                eventValue = self.parseCalendarEvent(self.calendarEvents[0])
                draw.text((2,339),eventValue,font=font20)
                draw.line((2,370,self.H-2,370),fill=0,width=3)
                
                eventValue = self.parseCalendarEvent(self.calendarEvents[1])
                draw.text((2,379),eventValue,font=font20)
                draw.line((2,410,self.H-2,410),fill=0,width=3)
                
                eventValue = self.parseCalendarEvent(self.calendarEvents[2])
                draw.text((2,419),eventValue,font=font20)
                draw.line((2,450,self.H-2,450),fill=0,width=3)
                
                eventValue = self.parseCalendarEvent(self.calendarEvents[3])
                draw.text((2,459),eventValue,font=font20)
                draw.line((2,490,self.H-2,490),fill=0,width=3)
                
                eventValue = self.parseCalendarEvent(self.calendarEvents[4])
                draw.text((2,499),eventValue,font=font20)
                draw.line((2,530,self.H-2,530),fill=0,width=3)
            
            # daily verse
            verseData = self.dailyBibleVerse
            reference = verseData['reference']
            w,h = font18.getsize(reference)
            draw.text(((self.H-w)/2,542),reference,font=font18)
            text = verseData['text']
            text = text.replace('\n','')
            lines = textwrap.wrap('"%s"'%text, width=50)
            y_text = 565
            for line in lines:
                width, height = font16.getsize(line)
                draw.text(((self.H - width) / 2, y_text), line, font=font16)
                y_text += height
            
            
            epd.display(epd.getbuffer(Limage))
            time.sleep(2)
            epd.sleep()
        except:
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            epd.sleep()
            exit()

    def drawCenteredText(self,draw,value,font,height,_fill=0):
        w,h = draw.textsize(value,font = font)
        weatherCtr = (((self.H-w)/2,height))
        draw.text(weatherCtr,value,font = font,fill = _fill)
    
    def drawOffsetText(self,draw,value,font,height,_fill=0,offset_frac):
        w,h = draw.textsize(value,font = font)
        weatherCtr = (((self.H-w)*offset_frac,height))
        draw.text(weatherCtr,value,font = font,fill = _fill)

    def parseCalendarEvent(self,event):
        start = event['start'].get('dateTime', event['start'].get('date'))
        startDateTime = datetime.datetime.strptime(start[:-6], '%Y-%m-%dT%H:%M:%S')
        startString = startDateTime.strftime('%a %m/%d %I:%M %p')
        summary = event['summary']
        return "%s %s" % (startString, summary[:20])

if __name__ == "__main__":
    def runCode():
        projDaily = ProjectDaily()
        projDaily.drawData()
    
    runCode()