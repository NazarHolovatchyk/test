import logging

from flask_restful import Api

from nh.smarty.app import setup_app
from nh.smarty.endpoints.automation import AutomationEndpoint
from nh.smarty.endpoints.system import SystemEndpoint
from nh.smarty.endpoints.status import Status

logging.basicConfig(level=logging.INFO)


def register_resources(_api):
    _api.add_resource(Status, '/v1/status')
    _api.add_resource(AutomationEndpoint, '/v1/automation')
    _api.add_resource(SystemEndpoint, '/v1/system/<string:device>')

app = setup_app()
api = Api(app)
# db = setup_database(app)
register_resources(api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=app.config['DEBUG'])
