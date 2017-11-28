import logging

from flask_restful import Api, Resource

from nh.smarty.app import setup_app
from nh.smarty.endpoints.actuator import ActuatorEndpoint
from nh.smarty.endpoints.scene import SceneEndpoint
from nh.smarty.endpoints.weather import WeatherEndpoint
from nh.smarty.endpoints.system import SystemEndpoint
from nh.smarty.endpoints.status import Status
from nh.smarty.endpoints.sensor import SensorEndpoint

logging.basicConfig(level=logging.INFO)


class Repos(Resource):
    def get(self):
        return ['test']


class Tags(Resource):
    def post(self):
        return {
            'tags': [
                {'test': '0.1'}
            ]
        }


def register_resources(_api):
    _api.add_resource(Status, '/v1/status')
    _api.add_resource(SceneEndpoint, '/v1/scene')
    _api.add_resource(WeatherEndpoint, '/v1/weather')
    _api.add_resource(ActuatorEndpoint, '/v1/actuator')
    _api.add_resource(SensorEndpoint, '/v1/sensor')
    _api.add_resource(SystemEndpoint, '/v1/system/<string:device>')
    _api.add_resource(Repos, '/v1/repos')
    _api.add_resource(Tags, '/v1/tags')


app = setup_app()
api = Api(app)
# db = setup_database(app)
register_resources(api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=app.config['DEBUG'], use_reloader=False)
