import logging

from nh.smarty.app import setup_app
from nh.smarty.broadlink_client.client import execute
from nh.smarty.devices.provider import RmBase

logger = logging.getLogger(__name__)


class ServiceError(Exception):
    pass


class BroadlinkService(object):

    def __init__(self):
        self.app = setup_app()

    def set_status(self, room, device, command):
        device_mapping = self.app.config['DEVICE_MAPPING']
        if room not in device_mapping:
            raise ValueError('Room not found')
        if device not in device_mapping[room]:
            raise ValueError('Device {} not found in {}'.format(device, room))
        hardware_id, device_name = device_mapping[room][device]

        if hardware_id.startswith('RM'):
            try:
                code = RmBase.get_code_from_file(device_name, command)
            except IOError as err:
                logger.error(err)
                raise ServiceError(err)
        else:
            code = command

        hardware = self.app.config['HARDWARE'][hardware_id]
        hardware_type = hardware['model']
        ip_addr = hardware['ip']
        mac_addr = hardware['mac']
        execute(hardware_type, ip_addr, mac_addr, code)
        return True
