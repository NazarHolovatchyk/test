import logging

from flask_restful import Api

from nh.alexa.app import setup_app
from nh.alexa.endpoints.automation import AutomationEndpoint
from nh.alexa.endpoints.status import Status

logging.basicConfig(level=logging.INFO)


def register_resources(_api):
    _api.add_resource(Status, '/v1/status')
    _api.add_resource(AutomationEndpoint, '/v1/automation')
    # _api.add_resource(ReputationTask, '/v1/ip/reputation/task/<string:task_name>')


app = setup_app()
api = Api(app)
# db = setup_database(app)
register_resources(api)

if __name__ == '__main__':
    app.run(port=5555, debug=app.config['DEBUG'])
