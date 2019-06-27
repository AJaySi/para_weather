# Each trigger represents the check if a set of conditions on certain 
# weather parameter values are met over certain geographic areas.
# Whenever a condition is met, an alert is fired and stored, 
# and can be retrieved by polling the API.

from pyowm import OWM
from pyowm.utils import geo
from pyowm.alertapi30.enums import WeatherParametersEnum, OperatorsEnum, AlertChannelsEnum
from pyowm.alertapi30.condition import Condition

def weather_alerts(owm_api, lat, lng):
    owm_obj = OWM(owm_api)
    am = owm_obj.alert_manager()

    # available types: Point, MultiPoint, Polygon, MultiPolygon
    geom_1 = geo.Point(lng, lat)

    # TBD: Alert should be cast over a wide area.
    # Alerts will have far reaching effects.
    #geom_1.geojson()
    #'''
    #{
    #  "type": "Point",
    #  "coordinates":[ lon, lat ]
    #}
    #'''
    # Pune - Mumbai - Satara - Pune
    # Indore - Nagpur - Hyderabad - Indore
    #geom_2 = geo.MultiPolygon([[73.856743, 18.520430], [72.877655, 19.075983]])

    # -- conditions --
    condition_1 = Condition(WeatherParametersEnum.TEMPERATURE,
                        OperatorsEnum.GREATER_THAN,
                        310.15)  # kelvin, 35C
    condition_2 = Condition(WeatherParametersEnum.CLOUDS,
                        OperatorsEnum.GREATER_THAN,
                        60) # clouds % coverage

    # create a trigger
    trigger = am.create_trigger(start_after_millis=355000, end_after_millis=487000,\
                            conditions=[condition_1, condition_2],\
                            area=[geom_1],\
                            alert_channel=AlertChannelsEnum.OWM_API_POLLING)

    # read all triggers
    triggers_list = am.get_triggers()
    print("Read all Weather triggers: {}".format(triggers_list))