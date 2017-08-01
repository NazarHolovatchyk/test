import argparse

from nh.smarty.devices.mapping import DEVICE_MAPPING


if __name__ == '__main__':
    parser = argparse.ArgumentParser('python cli.py', description='Broadlink CLI')
    parser.add_argument("-r", "--room", dest="room", default='house', help="Room name")
    parser.add_argument("-d", "--device", dest="device", help="Device name")
    parser.add_argument("-c", "--command", dest='command', required=False, help="Command")
    parsed = parser.parse_args()

    device = DEVICE_MAPPING[parsed.room][parsed.device]
    device.send(parsed.command)
