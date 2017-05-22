#!/home/pi/domoticz/venv/bin/python
"""
Support for Broadlink devices.
"""
import argparse
import logging
import os
import socket
import time
import sys
from base64 import b64encode, b64decode
from datetime import datetime, timedelta

import broadlink


logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 10
DEFAULT_RETRY = 2
SERVICE_LEARN = "learn_command"
SERVICE_SEND = "send_packet"

RM_TYPES = ["rm", "rm2", "rm_mini", "rm_pro_phicomm", "rm2_home_plus",
            "rm2_home_plus_gdt", "rm2_pro_plus", "rm2_pro_plus2",
            "rm2_pro_plus_bl", "rm_mini_shate"]
SP1_TYPES = ["sp1"]
SP2_TYPES = ["sp2", "honeywell_sp2", "sp3", "spmini2", "spminiplus"]

SWITCH_TYPES = RM_TYPES + SP1_TYPES + SP2_TYPES


class BroadlinkBase(object):
    """Representation of a basic Broadlink device"""

    def __init__(self, device=None):
        self._device = device

    def learn_command(self):
        try:
            auth = self._device.auth()
        except socket.timeout:
            logger.error("Failed to connect to device, timeout.")
            return False
        if not auth:
            logger.error("Failed to connect to device.")
            return False

        self._device.enter_learning()

        logger.info("Press the key you want to learn")
        start_time = datetime.utcnow()
        while (datetime.utcnow() - start_time) < timedelta(seconds=10):
            packet = self._device.check_data()
            if packet:
                log_msg = 'Received packet is: {}'.format(b64encode(packet).decode('utf8'))
                logger.info(log_msg)
                return True
            time.sleep(0.1)
        logger.error('Did not received any signal')
        return False

    @staticmethod
    def _get_payload(packet):
        payload = b64decode(packet)
        return payload

    def _send_data(self, packet, retry=DEFAULT_RETRY):
        try:
            self._device.send_data(self._get_payload(packet))
        except (socket.timeout, ValueError) as err:
            if retry < 1:
                logger.error("Failed to send packet to device: {}".format(err))
                return False
            self._send_data(packet, retry=retry - 1)
        return True

    def auth(self, retry=DEFAULT_RETRY):
        try:
            auth_result = self._device.auth()
        except socket.timeout:
            auth_result = False
        if not auth_result and retry > 0:
            return self.auth(max(0, retry-1))
        return auth_result


class BroadlinkRMSwitch(BroadlinkBase):
    """Representation of an Broadlink RM device"""

    def __init__(self, ip_addr, mac_addr):
        """Initialize the switch."""
        device = broadlink.rm((ip_addr, 80), mac_addr)
        super(BroadlinkRMSwitch, self).__init__(device)

    def send(self, packet):
        """Send packet to device."""
        self._device.send_data(packet)


class BroadlinkSP1Switch(BroadlinkBase):
    """Representation of an Broadlink switch."""

    def __init__(self, ip_addr, mac_addr):
        """Initialize the switch."""
        device = broadlink.sp1((ip_addr, 80), mac_addr)
        super(BroadlinkSP1Switch, self).__init__(device)
        # self._command_on = 1
        # self._command_off = 0

    @staticmethod
    def _get_payload(packet):
        if packet in [1, '1', 'true', 'on']:
            payload = 1
        elif packet in [0, '0', 'false', 'off']:
            payload = 0
        else:
            raise ValueError('Invalid command')
        return payload

    def _sendpacket(self, packet, retry=2):
        """Send packet to device."""
        try:
            self._device.set_power(packet)
        except (socket.timeout, ValueError) as error:
            if retry < 1:
                logger.error(error)
                return False
            if not self.auth():
                return False
            return self._sendpacket(packet, max(0, retry-1))
        return True


class BroadlinkSP2Switch(BroadlinkBase):
    """Representation of an Broadlink switch."""

    def __init__(self, device):
        """Initialize the switch."""
        device = broadlink.sp2((ip_addr, 80), mac_addr)
        super(BroadlinkSP2Switch, self).__init__(device)

    @property
    def assumed_state(self):
        """Return true if unable to access real state of entity."""
        return False

    @property
    def should_poll(self):
        """Polling needed."""
        return True

    def update(self):
        """Synchronize state with switch."""
        self._update()

    def _update(self, retry=2):
        try:
            state = self._device.check_power()
        except (socket.timeout, ValueError) as error:
            if retry < 1:
                logger.error(error)
                return
            if not self.auth():
                return
            return self._update(max(0, retry-1))
        if state is None and retry > 0:
            return self._update(max(0, retry-1))
        self._state = state

DEVICES = {
    'RM_PRO': {'ip': '192.168.1.201', 'mac': 'B4:43:0D:FB:C9:F5', 'model': 'rm'},
    'RM_MINI_1': {'ip': '192.168.1.203', 'mac': 'B4:43:0D:EF:AD:BE', 'model': 'rm'},
    'RM_MINI_2': {'ip': '192.168.1.205', 'mac': 'B4:43:0D:EF:AD:B7', 'model': 'rm'},
    'SP2_LR_CAB': {'ip': '192.168.1.202', 'mac': '34:EA:34:F1:B0:67', 'model': 'sp2'},
    'SP2_CR_IRON': {'ip': '192.168.1.204', 'mac': '34:EA:34:E4:05:A5', 'model': 'sp2'},
    'SP2_K_COOK': {'ip': '192.168.1.206', 'mac': '34:EA:34:F1:AC:39', 'model': 'sp2'}
}


if __name__ == '__main__':
    # python broadlink_cli.py rm -i 192.168.1.201 -m B4:43:0D:FB:C9:F5 -c JgBIAA==
    parser = argparse.ArgumentParser('python broadlink.py', description='Broadlink CLI')
    parser.add_argument("device", help="Device name [rm, sp2, etc.]")
    parser.add_argument("-i", "--ip", dest='ip', required=False, help="IP address. E.g. 10.10.10.10")
    parser.add_argument("-m", "--mac", dest='mac', required=False, help="MAC address. E.g. AA:BB:CC:DD:EE:FF")
    parser.add_argument("-c", "--command", dest='command', required=False, help="Command")
    parser.add_argument("-f", "--filename", dest='filename', required=False, help="File with command")
    # parser.add_argument("-d", "--device", dest='device', required=False, help="Device name")
    parsed = parser.parse_args()

    if parsed.device in DEVICES:
        dev = DEVICES[parsed.device]
        device = dev['model']
        ip_addr = dev['ip']
        mac_addr = dev['mac']
    else:
        device = parsed.device
        ip_addr = parsed.ip
        # mac_addr = binascii.unhexlify(parsed.mac.encode().replace(b':', b' '))
        mac_addr = bytearray.fromhex(parsed.mac.replace(':', ' '))

    command = parsed.command
    if not command:
        base_path = os.path.dirname(os.path.realpath(__file__))
        print(base_path)
        cmd_path = '{}/cmd/{}.txt'.format(base_path, parsed.filename)
        with open(cmd_path, 'r') as f:
            command = f.read()

    if device in RM_TYPES:
        # broadlink_device = BroadlinkRMSwitch((ip_addr, 80), mac_addr)
        device = broadlink.rm((ip_addr, 80), mac_addr)
        device.auth()
        device.send_data(b64decode(command))
    elif device in SP2_TYPES:
        device = broadlink.sp2((ip_addr, 80), mac_addr)
        device.auth()
        status = 1 if command.lower() in ['on', '1', 'yes', 'true'] else 0
        device.set_power(status)
    else:
        raise ValueError('Unknown device. Available: rm, sp2 and {}'.format(DEVICES.keys()))

    # try:
    #     auth = broadlink_device.auth()
    # except socket.timeout as err:
    #     raise IOError("Failed to connect to device: {}".format(err))
    # if not auth:
    #     raise IOError("Failed to authenticate to device")

    # if parsed.command == 'send':

