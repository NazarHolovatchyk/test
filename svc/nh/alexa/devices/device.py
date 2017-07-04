from nh.alexa.devices import provider


class Device(object):

    def send(self, cmd):
        self.hardware.send(cmd)


class LivingroomLight(Device):

    def __init__(self):
        self.hardware = provider.Sp2LrCab()

