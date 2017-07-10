import os

from flask import Flask


instance = None


def setup_app(environment=None):
    global instance
    if instance:
        return instance

    app = Flask(__name__)
    if not environment:
        environment = os.environ.get('ALEXA_SVC_ENV', 'base')
    config_class = 'nh.smarty.settings.{}.Config'.format(environment)
    app.config.from_object(config_class)
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_envvar("APP_CONFIG", silent=True)

    instance = app
    return app
