"""
Support for Broadlink devices.
"""
import logging
import socket
import time
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
        self.device = device

    def learn_command(self):
        try:
            auth = self.device.auth()
        except socket.timeout:
            logger.error("Failed to connect to device, timeout.")
            return False
        if not auth:
            logger.error("Failed to connect to device.")
            return False

        self.device.enter_learning()

        logger.info("Press the key you want to learn")
        start_time = datetime.utcnow()
        while (datetime.utcnow() - start_time) < timedelta(seconds=10):
            packet = self.device.check_data()
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
            self.device.send_data(self._get_payload(packet))
        except (socket.timeout, ValueError) as err:
            if retry < 1:
                logger.error("Failed to send packet to device: {}".format(err))
                return False
            self._send_data(packet, retry=retry - 1)
        return True

    def auth(self, retry=DEFAULT_RETRY):
        try:
            auth_result = self.device.auth()
        except socket.timeout:
            auth_result = False
        if not auth_result and retry > 0:
            return self.auth(max(0, retry - 1))
        return auth_result


class BroadlinkRMSwitch(BroadlinkBase):
    """Representation of an Broadlink RM device"""

    def __init__(self, ip_addr, mac_addr):
        """Initialize the switch."""
        device = broadlink.rm((ip_addr, 80), mac_addr)
        super(BroadlinkRMSwitch, self).__init__(device)

    def send(self, command):
        """Send packet to device."""
        self.device.auth()
        packet = b64decode(command)
        self.device.send_data(packet)


class BroadlinkSP1Switch(BroadlinkBase):
    """Representation of an Broadlink switch."""

    def __init__(self, ip_addr, mac_addr):
        """Initialize the switch."""
        device = broadlink.sp1((ip_addr, 80), mac_addr)
        super(BroadlinkSP1Switch, self).__init__(device)

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
            self.device.set_power(packet)
        except (socket.timeout, ValueError) as error:
            if retry < 1:
                logger.error(error)
                return False
            if not self.auth():
                return False
            return self._sendpacket(packet, max(0, retry - 1))
        return True


class BroadlinkSP2Switch(BroadlinkBase):
    """Representation of an Broadlink SP2 switch."""

    def __init__(self, ip_addr, mac_addr):
        """Initialize the switch."""
        self.device = broadlink.sp2((ip_addr, 80), mac_addr)
        super(BroadlinkSP2Switch, self).__init__(self.device)

    def send(self, command):
        self.device.auth()
        if str(command).lower() in ['on', '1', 'yes', 'true']:
            status = 1
        elif str(command).lower() in ['off', '0', 'no', 'false']:
            status = 0
        else:
            raise ValueError('Unknown command: {}'.format(command))
        self.device.set_power(status)

    def get_status(self):
        """Synchronize state with switch."""
        return self._update()

    def _update(self, retry=2):
        try:
            state = self.device.check_power()
        except (socket.timeout, ValueError) as error:
            if retry < 1:
                logger.error(error)
                raise IOError('Cannot get status. Max retries exceeded.')
            if not self.auth():
                raise IOError('Cannot get status. Device authentication failed.')
            return self._update(max(0, retry - 1))
        if state is None and retry > 0:
            return self._update(max(0, retry - 1))
        return state


def execute(device_type, ip_addr, mac_addr, command):
    if device_type in RM_TYPES:
        # broadlink_device = BroadlinkRMSwitch((ip_addr, 80), mac_addr)
        device_type = broadlink.rm((ip_addr, 80), mac_addr)
        device_type.auth()
        device_type.send_data(b64decode(command))
    elif device_type in SP2_TYPES:
        device_type = broadlink.sp2((ip_addr, 80), mac_addr)
        device_type.auth()
        status = 1 if command.lower() in ['on', '1', 'yes', 'true'] else 0
        device_type.set_power(status)
    else:
        raise ValueError('Unknown device. Available: rm, sp2')
