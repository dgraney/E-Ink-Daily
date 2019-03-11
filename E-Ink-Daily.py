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

        #self.drawData()

    def drawData(self):
        try:
            epd = epd7in5.EPD()
            epd.init()
            print("Clear")
            epd.Clear(0xFF)

            print("Drawing")
            W = epd7in5.EPD_WIDTH
            H = epd7in5.EPD_HEIGHT
            Limage = Image.new("1",( H,W ),255)
            draw = ImageDraw.Draw(Limage)
            font65 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 65)
            font48 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 48)
            font36 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 36)
            font24 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 24)
            font18 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 18)
            todayWeatherData = self.weatherData.dailyWeather[0]
            ts = int(todayWeatherData.TimeStamp)
            weekDay = datetime.date.fromtimestamp(ts).strftime('%A')
            date = datetime.date.fromtimestamp(ts).strftime('%m/%d/%Y')
            w,h = draw.textsize(weekDay,font65)
            weekDayCtr = ((H-w)/2,(W-h)/2)
            draw.text(weekDayCtr,weekDay,font = font65,fill = 0)
            draw.text((2,75),date,font = font48,fill = 0)
            epd.display(epd.getbuffer(Limage))
            time.sleep(2)
        except:
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            exit()

if __name__ == "__main__":
    projDaily = ProjectDaily()
    projDaily.drawData()