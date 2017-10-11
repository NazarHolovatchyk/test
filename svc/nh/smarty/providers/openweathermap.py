import json
from datetime import datetime

from pyowm import OWM

from nh.smarty.providers.base_briefing import BaseBriefing

DEGREE_CHAR = u'\xB0'


class OWMBriefing(object):
    """
    {
      "status": "Clouds",
      "visibility_distance": null,
      "humidity": 71,
      "clouds": 12,
      "temperature": {
        "min": 292.97,
        "max": 301.75,
        "eve": 300.74,
        "morn": 300.15,
        "night": 292.97,
        "day": 300.15
      },
      "dewpoint": null,
      "snow": {},
      "detailed_status": "few clouds",
      "reference_time": 1505124000,
      "weather_code": 801,
      "humidex": null,
      "rain": {},
      "sunset_time": 0,
      "pressure": {
        "press": 989.5,
        "sea_level": null
      },
      "sunrise_time": 0,
      "heat_index": null,
      "weather_icon_name": "02d",
      "wind": {
        "speed": 5.22,
        "deg": 149
      }
    }
    """

    def __init__(self, api_key):
        self.api_key = api_key

    def get_data(self, location):
        owm = OWM(API_key=self.api_key)
        forecaster = owm.daily_forecast(location)
        forecast_json = forecaster.get_forecast().to_JSON()
        forecast = json.loads(forecast_json)

        briefing = []
        for day_forecast in forecast['weathers']:
            dt = datetime.fromtimestamp(day_forecast['reference_time'])
            title = dt.strftime('%A %B %d')
            status = day_forecast['detailed_status']
            tmin = self.kelvin2celsius(day_forecast['temperature']['min'])
            tmax = self.kelvin2celsius(day_forecast['temperature']['max'])
            wind = int(day_forecast['wind']['speed'])
            pressure = int(day_forecast['pressure']['press'])
            text = u'{status}. Temperature from {tmin}{deg} to {tmax}{deg} Celsius. ' \
                   u'Wind {wind} meters per second. Pressure {pressure} hPa'.format(
                status=status,
                tmin=tmin,
                tmax=tmax,
                deg=DEGREE_CHAR,
                wind=wind,
                pressure=pressure
            )
            briefing.append({'title': title, 'text': text})

        return briefing

    @staticmethod
    def kelvin2celsius(t):
        return int(round(float(t) - 273.15))
