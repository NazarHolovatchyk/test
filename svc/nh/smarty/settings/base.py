import os


class Config(object):

    DEBUG = bool(os.environ.get('DEBUG', True))

    BASE_DIR = os.path.realpath(os.path.dirname(__file__) + '/../../..')

    PYTHON_BIN = BASE_DIR + '/venv/bin/python'

    BROADLINK_CMD_PATH = BASE_DIR + '/nh/smarty/providers/broadlink_cmd'

    OPEN_WEATHER_MAP_API_KEY = 'd85a4d69c3b70ae65ead6c20bf0e343e'
