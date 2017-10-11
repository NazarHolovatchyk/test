from nh.smarty.endpoints.base import BaseResource
from nh.smarty.app import setup_app

app = setup_app()


class FlashBriefingEndpoint(BaseResource):

    WHITELIST = ['weather']

    def get(self, name):
        if name not in self.WHITELIST:
            return self.error_response('Unknown briefing name')

        cached = int(self.get_param('cached', required=False, default=1))
        if cached:
            file_path = app.config['STATIC_DIR'] + '/{}.json'.format(name)
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
            except IOError as err:
                return self.error_response(err, status=501)
        else:
            try:
                content = self.get_briefing(name)
            except ValueError as err:
                return self.error_response(err, status=400)
            except Exception as err:
                return self.error_response(err, status=501)

        return self.success_response(content, raw=True)

    @classmethod
    def get_briefing(cls, briefing_name):
        if briefing_name == 'weather':
            from nh.smarty.providers.openweathermap import OWMBriefing
            api_key = app.config['OPEN_WEATHER_MAP_API_KEY']
            return OWMBriefing(api_key)
        raise ValueError('Unknown briefing')
