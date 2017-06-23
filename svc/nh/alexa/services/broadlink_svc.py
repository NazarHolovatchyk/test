import logging

from nh.alexa.app import setup_app
from nh.alexa.broadlink_client.client import execute, get_command_from_file

logger = logging.getLogger(__name__)


class ServiceError(Exception):
    pass


ROOM_MAPPING = {
    'livingroom': {

    },
    'bedroom': {

    },
    'childroom': {

    },
    'kitchen': {

    },
    'all': {

    }
}


class BroadlinkService(object):

    def __init__(self):
        self.app = setup_app()

    def set_status(self, room, device, command):
        hardware = self.app.config['HARDWARE_MAPPING'][device]

        if hardware.startswith('RM'):
            filename = '{}/{}_{}.txt'.format(self.app.config['BROADLINK_CMD_PATH'], device, command)
            try:
                code = get_command_from_file(filename)
            except IOError as err:
                logger.error(err)
                raise ServiceError(err)
        else:
            code = command

        dev = self.app.config['HARDWARE'][hardware]
        device_type = dev['model']
        ip_addr = dev['ip']
        mac_addr = dev['mac']
        execute(device_type, ip_addr, mac_addr, code)
        return True
