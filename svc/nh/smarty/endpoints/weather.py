from nh.smarty.app import setup_app
from nh.smarty.endpoints.base import BaseResource
from nh.smarty.providers.openweathermap import OWMBriefing

app = setup_app()


class WeatherEndpoint(BaseResource):

    def get(self):
        api_key = app.config['OPEN_WEATHER_MAP_API_KEY']
        location = 'lviv,ua'
        try:
            owm = OWMBriefing(api_key)
            content = owm.get_data(location)
        except ValueError as err:
            return self.error_response(err, status=400)
        except Exception as err:
            return self.error_response(err, status=501)

        return self.success_response(content)
