import logging

from nh.smarty.app import setup_app
from nh.smarty.providers import broadlink_provider

app = setup_app()


class RmBase(object):
    model = 'rm'
    ip = None
    mac = None

    def __init__(self, device_name):
        self.hardware = broadlink_provider.BroadlinkRMSwitch(self.ip, self.mac)
        self.device_name = device_name

    def send(self, command):
        try:
            code = self.get_code_from_file(self.device_name, command)
        except IOError as err:
            msg = 'Command {} for {} device not found'.format(command, self.device_name)
            logging.error(msg + '\n' + str(err))
            raise ValueError(msg)
        return self.hardware.send(code)

    @staticmethod
    def get_code_from_file(device, command):
        filename = '{}/{}_{}.txt'.format(app.config['BROADLINK_CMD_PATH'], device, command)
        with open(filename, 'r') as f:
            code = f.read()
        return code


class RmPro(RmBase):
    ip = '192.168.1.201'
    mac = 'B4:43:0D:FB:C9:F5'


class RmMini1(RmBase):
    ip = '192.168.1.203'
    mac = 'B4:43:0D:EF:AD:BE'


class RmMini2(RmBase):
    ip = '192.168.1.205'
    mac = 'B4:43:0D:EF:AD:B7'


class Sp2Base(object):
    ip = None
    mac = None

    def __init__(self):
        self.device = broadlink_provider.BroadlinkSP2Switch(self.ip, self.mac)

    def send(self, cmd):
        return self.device.send(cmd)


class Sp2LrCab(Sp2Base):
    """Livingroom Cabinet light"""
    ip = '192.168.1.202'
    mac = '34:EA:34:F1:B0:67'


class Sp2Iron(Sp2Base):
    """Iron power socket"""
    ip = '192.168.1.204'
    mac = '34:EA:34:E4:05:A5'


class Sp2Doorbell(Sp2Base):
    """Doorbell power socket"""
    ip = '192.168.1.206'
    mac = '34:EA:34:F1:AC:39'
