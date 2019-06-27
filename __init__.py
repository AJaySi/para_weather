from mycroft import MycroftSkill, intent_file_handler
from pyowm import OWM

# FixMe: These need to go into a config file.
owm_api = '843a73d5385a861cabc4088c0ca45dea'
darksky_api = ''
windy_api = ''


class ParaglidingWeather(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('weather.paragliding.intent')
    def handle_weather_paragliding(self, message):
        self.speak_dialog('weather.paragliding')


def create_skill():
    return ParaglidingWeather()

