from nh.smarty.endpoints.base import BaseResource
from nh.smarty.app import setup_app

app = setup_app()


class FlashBriefingEndpoint(BaseResource):

    def get(self, name):
        try:
            briefing = self.get_briefing(name)
            data = briefing.get_data()
        except Exception as err:
            return self.error_response(err)

        return self.success_response(data)

    @classmethod
    def get_briefing(cls, briefing_name):
        if briefing_name == 'weather':
            from nh.smarty.providers.openweathermap import OWMBriefing
            api_key = app.config['OPEN_WEATHER_MAP_API_KEY']
            return OWMBriefing(api_key)
        raise ValueError('Unknown briefing')
