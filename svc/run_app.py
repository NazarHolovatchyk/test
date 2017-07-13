import logging

from flask_restful import Api

from nh.smarty.app import setup_app
from nh.smarty.endpoints.automation import AutomationEndpoint
from nh.smarty.endpoints.actuator import ActuatorEndpoint
from nh.smarty.endpoints.scene import SceneEndpoint
from nh.smarty.endpoints.system import SystemEndpoint
from nh.smarty.endpoints.status import Status
from nh.smarty.endpoints.sensor import SensorEndpoint

logging.basicConfig(level=logging.INFO)


def register_resources(_api):
    _api.add_resource(Status, '/v1/status')
    _api.add_resource(ActuatorEndpoint, '/v1/actuator')
    _api.add_resource(SensorEndpoint, '/v1/sensor')
    _api.add_resource(SceneEndpoint, '/v1/scene')
    _api.add_resource(SystemEndpoint, '/v1/system/<string:device>')
    _api.add_resource(AutomationEndpoint, '/v1/automation')

app = setup_app()
api = Api(app)
# db = setup_database(app)
register_resources(api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=app.config['DEBUG'])
