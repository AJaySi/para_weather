import re
import ConfigParser
import os 
import requests

# Group 2xx: Thunderstorm
thunderstrom = {
    200: "Thunderstorm with light rain",
    201: "Thunderstorm with rain",
    202: "Thunderstorm with heavy rain",
    210: "Thunderstorm (Light)",
    211: "Thunderstorm",
    212: "Heavy thunderstorm",
    221: "Ragged thunderstorm",
    230: "Thunderstorm with light drizzle",
    231: "Thunderstorm with drizzle",
    232: "Thunderstorm with heavy drizzle"
}
    
# Group 3xx: Drizzle
drizzle = {
    300: "Drizzle: light intensity",
    301: "Drizzle",
    302: "Drizzle: heavy intensity",
    310: "Drizzle: light intensity drizzle rain",
    311: "Drizzle: drizzle rain",
    312: "Drizzle: heavy intensity drizzle rain",
    313: "Drizzle: shower rain and drizzle",
    314: "Drizzle: heavy shower rain and drizzle",
    321: "Drizzle: shower drizzle"
}
    
#Group 5xx: Rain
rain = { 
    500: "Rain: Light rain",
    501: "Rain: Moderate rain",
    502: "Rain: Heavy intensity rain",
    503: "Rain: Very heavy rain",
    504: "Rain: Extreme rain",
    511: "Rain: Freezing rain",
    520: "Rain: Light intensity shower rain",
    521: "Rain: Shower rain",
    522: "Rain: Heavy intensity shower rain",
    531: "Rain: Ragged shower rain"
}
    
# Group 7xx: Atmosphere
atmosphere = {
    701: "Atmosphere: Mist",
    711: "Atmosphere: Smoke",
    721: "Atmosphere: Haze",
    731: "Atmosphere: Dust whirls",
    741: "Atmosphere: Fog",
    751: "Atmosphere: Sand",
    761: "Atmosphere: Dust",
    762: "Atmosphere: Ash volcanic",
    771: "Atmosphere: Squall",
    781: "Atmosphere: Tornado"
}
    
    
#Group 80x: Clouds
clouds = {
    800: "Clear Sky",
    801: "Clouds: Few clouds: 11-25%",
    802: "Clouds: Scattered clouds: 25-50%",
    803: "Clouds: Broken clouds: 51-84%",
    804: "Clouds: Overcast clouds: 85-100%"
}


# Beaufort WindScale
wind_scale = {
    xrange(1): "Calm Light Wind",
    xrange(1, 5): "Light Wind",
    xrange(6, 11): "Light Breeze/Wind",
    xrange(12, 19): "Gentle Breeze",
    xrange(20, 28): "Moderate Breeze",
    xrange(29, 38): "Fresh Breeze",
    xrange(39, 49): "Strong Gale/Wind",
    xrange(50, 61): "Strong Breeze/Wind",
    xrange(62, 74): "Fresh Gale",
    xrange(75, 88): "Stong Gale",
    xrange(89, 102): "Whole Gale",
    xrange(103, 117): "Storm",
    xrange(117, 200): "Hurricane"
}

# METAR Sky Conditions
sky_conditions = {
    'BKN' : "Broken cloud layer 5/8ths to 7/8ths",
    'CB' : "Cumulonimbus",
    'CLR' : "Sky clear at or below 12,000AGL",
    'FEW' : "Few cloud layer 0/8ths to 2/8ths",
    'OVC' : "Overcast cloud layer 8/8ths coverage",
    'SCT' : "Scattered cloud layer 3/8ths to 4/8ths", 
    'SKC' : "Sky Clear",
    'TCU' : "Towering Cumulus"
}

# METAR Flight Codes
flight_category = {
    'LIFR' : "Low Instrument Flight Rules(LIFR). Ceiling: below 500 feet AGL, Visibility: less than 1 mile",
    'IFR' : "Instrument Flight Rules(IFR)	Ceiling: 500 to below 1,000 feet AGL, Visibility: 1 mile to less than 3 miles",
    'MVFR' : "Marginal Visual Flight Rules(MVFR) Ceiling: 1,000 to 3,000 feet AGL, Visibility: 3 to 5 miles",
    'VFR' : "Visual Flight Rules(VFR)	Ceiling: greater than 3,000 feet AGL, Visibility: and greater than 5 miles"
}

# Common function to return the value for the given key in the dict.
def find_val(st_cod, st_dict):
    for st_code, st_msg in st_dict.items():
        if st_cod == st_code:
            return(st_msg)


# Forecast Series Data for analysis.
def series_data(series_lst):
    pass
    # For each of forecast object get all the details.
    #for aseries in series_lst:
    #    for adata in aseries:


# Function to classify wind speen in kmph to wind scale.
def windscale(wnd):
    for key in wind_scale:
        if wnd in key:
            return(wind_scale[key])


# Check the return weather status code and meaning for the same.    
def desc_code(str_code):
    w_code = str(str_code)

    if re.search(r'^2\d\d', w_code):
        return(find_val(str_code, thunderstorm))
    elif re.search(r'^3\d\d', w_code):
        return(find_val(str_code, drizzle))
    # 5xx: Rain status codes
    elif re.search(r'^5\d\d', w_code):
        return(find_val(str_code, rain))
    elif re.search(r'^7\d\d', w_code):
        return(find_val(str_code, atmosphere))
    elif re.search(r'^8\d\d',w_code):
        return(find_val(str_code, clouds))


# Utility function to convert direction degress to directions.
def wind_direction(wind_deg, taf=''):
    # There is an angle change at every 22.5 degrees, 
    # the direction should swap hands after 11.25 degrees.
    # Using values from 327-348 (The entire NNW spectrum)
    if 'taf' not in taf: 
        val = wind_deg.get('deg')
    else:
        val = wind_deg

    val = int((val/22.5)+.5)
    wind_direction_arr=["North(N)","North northEast(NNE)","North East(NE)",\
        "East NorthEast(ENE)","East(E)","East SouthEast(ESE)", "South East(SE)",\
        "South SouthEast(SSE)","South(S)","South SouthWest(SSW)","South West(SW)",\
        "West SouthWest(WSW)","West(W)","West NorthWest(WNW)","North West(NW)",\
        "North NorthWest(NNW)"]

    # Divide the angle by 22.5 because 360deg/16 
    # directions = 22.5deg/direction change
    return(wind_direction_arr[val % 16])


# Utility function to convert mph to kmph
def mph_to_kmph(mph):
    """
    When Converting m/sec to km/hr, divide the speed with 
    1000 and multiply the result with 3600.
    """
    return (3.6 * mph)


# Utility function to calucalte the cloudbase height,
# when surface temperature and dewpoint is given.
def cal_cloudbase(temp, dew, elevation=0):
   # calculate a cloud base:
   # 1. difference between the temperature at the surface and the dew point
   temp_diff = temp - dew
   # Divide the difference by 2.5
   # Multiply the result by 1,000
   # In Celcius and kilometers.

   cloudbase = (temp_diff / 2.5) * 1000
   cloudbase = cloudbase * 0.3048
   cloudbase += get_elevation()
   return(int(cloudbase))


# Utility function to get the elevation for cloudbase calculations
def get_elevation():

    checkwx_api = get_api_key('checkwx')
    hdr = { 'X-API-Key': checkwx_api }
    response = requests.get('https://api.checkwx.com/station/vapo', headers=hdr).json()
    # Return the elevation for cloudbase calculations.
    return(response['data'][0]['elevation']['meters'])


# Utility function to remove duplicate words from the string
def unique_wrds(lst):
    ulist = []
    [ulist.append(x) for x in lst if x not in ulist]
    return ulist


# Utility function to return the api key from config file
def get_api_key(flag):
    config = ConfigParser.ConfigParser()
    # Needs absolute path.
    conf = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config_api')
    config.read(conf)

    if 'owm' in flag:
        return(config.get('openweathermap', 'api').rstrip())
    elif 'darksky' in flag:
        return(config.get('darksky', 'api').rstrip())
    elif 'worldweatheronline' in flag:
        return(config.get('worldweatheronline', 'api').rstrip())
    elif 'checkwx' in flag:
        return(config.get('checkwx_api', 'api').rstrip())
    elif 'windy' in flag:
        return(config.get('windy', 'api').rstrip())