import os


class Config(object):

    DEBUG = bool(os.environ.get('DEBUG', True))

    BASE_DIR = os.path.realpath(os.path.dirname(__file__) + '/../../..')

    PYTHON_BIN = BASE_DIR + '/venv/bin/python'

    HARDWARE = {
        'RM_PRO': {'ip': '192.168.1.201', 'mac': 'B4:43:0D:FB:C9:F5', 'model': 'rm'},
        'RM_MINI_1': {'ip': '192.168.1.203', 'mac': 'B4:43:0D:EF:AD:BE', 'model': 'rm'},
        'RM_MINI_2': {'ip': '192.168.1.205', 'mac': 'B4:43:0D:EF:AD:B7', 'model': 'rm'},
        'SP2_LR_CAB': {'ip': '192.168.1.202', 'mac': '34:EA:34:F1:B0:67', 'model': 'sp2'},
        'SP2_CR_IRON': {'ip': '192.168.1.204', 'mac': '34:EA:34:E4:05:A5', 'model': 'sp2'},
        'SP2_K_COOK': {'ip': '192.168.1.206', 'mac': '34:EA:34:F1:AC:39', 'model': 'sp2'}
    }

    HARDWARE_MAPPING = {
        'intelite': 'RM_MINI_1',
        'intelite2': 'RM_MINI_2',
        'apple_tv': 'RM_PRO',
        'lg_tv': 'RM_PRO',
        'pioneer': 'RM_PRO',
        'cabinet': 'SP2_LR_CAB',
        'iron': 'SP2_CR_IRON',
        'cooking': 'SP2_K_COOK',
        'sony_tv': 'RM_MINI_2'
    }
    DEVICE_MAPPING = {
        'global': {
            'light': ['SP2_LR_CAB', None],
            'tv': ['RM_PRO', 'lg_tv'],
            'apple': ['RM_PRO', 'apple_tv'],
            'audio': ['RM_PRO', 'pioneer']
        },
        'livingroom': {
            'light': ['SP2_LR_CAB', None],
            'tv': ['RM_PRO', 'lg_tv'],
            'apple': ['RM_PRO', 'apple_tv'],
            'audio': ['RM_PRO', 'pioneer']
        },
        'bedroom': {
            'light': ['RM_MINI_1', 'intelite']
        },
        'childroom': {
            'light': ['RM_MINI_2', 'intelite'],
            'tv': ['RM_MINI_2', 'sony_tv']
        },
        'kitchen': {

        },
        'bathroom': {

        },
        'cabinet': {

        }
    }

    SCENES = {
        'movie': [
            {'room': '', 'device': '', 'status': ''}
        ]
    }

    BROADLINK_CMD_PATH = BASE_DIR + '/nh/alexa/broadlink_client/cmd'
