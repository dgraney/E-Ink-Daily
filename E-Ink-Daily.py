import scripts.quickStart as calendar
import scripts.dailyVerse as dailyVerse
import scripts.weather as weather

class projectDaily():
    def __init__ (self):
        self.dailyBibleVerse = dailyVerse.getDailyVerse()
        self.weatherData = weather.main()
        self.calendarEvents = calendar.main()