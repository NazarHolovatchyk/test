from nh.smarty.devices.bmp180 import BMP180
from nh.smarty.devices.broadlink_dev import RmPro, RmMini1, RmMini2, Sp2LrCab, Sp2Iron, Sp2Doorbell
from nh.smarty.devices.utils import Delay


DEVICE_MAPPING = {
    'house': {
        'light': Sp2LrCab(),
        'tv': RmPro('lg_tv'),
        'apple': RmPro('apple_tv'),
        'audio': RmPro('pioneer'),
        'iron': Sp2Iron(),
        'door': Sp2Doorbell(),
        'delay': Delay()
    },
    'livingroom': {
        'light': Sp2LrCab(),
        'tv': RmPro('lg_tv'),
        'apple': RmPro('apple_tv'),
        'audio': RmPro('pioneer')
    },
    'bedroom': {
        'light': RmMini1('intelite')
    },
    'childroom': {
        'light': RmMini2('intelite'),
        'tv': RmMini1('sony_tv'),
        'iron': Sp2Iron()
    },
    'kitchen': {},
    'bathroom': {},
    'cabinet': {}
}

DEVICE_MAPPING['house']['television'] = DEVICE_MAPPING['house']['tv']
DEVICE_MAPPING['livingroom']['television'] = DEVICE_MAPPING['livingroom']['tv']

SENSOR_MAPPING = {
    'house': {
        'temperature': BMP180(),
        'pressure': BMP180('pressure')
    },
    'livingroom': {
        'temperature': BMP180('temperature'),
        'pressure': BMP180('pressure')
    },
    'bedroom': {},
    'childroom': {},
    'kitchen': {},
    'bathroom': {},
    'cabinet': {}
}
