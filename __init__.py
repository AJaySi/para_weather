from mycroft import MycroftSkill, intent_file_handler


class ParaglidingWeather(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('weather.paragliding.intent')
    def handle_weather_paragliding(self, message):
        self.speak_dialog('weather.paragliding')


def create_skill():
    return ParaglidingWeather()

