import os


class Config(object):

    DEBUG = bool(os.environ.get('DEBUG', True))

    BASE_DIR = os.path.realpath(os.path.dirname(__file__) + '/../../..')

    PYTHON_BIN = BASE_DIR + '/venv/bin/python'

    BROADLINK_CMD_PATH = BASE_DIR + '/nh/smarty/providers/broadlink_cmd'
