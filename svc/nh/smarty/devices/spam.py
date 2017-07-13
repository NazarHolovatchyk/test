from nh.smarty.providers import broadlink_provider


class Device(object):
    def send(self, cmd=''):
        self.hardware.send(cmd)


class LivingroomLight(Device):
    def __init__(self):
        self.hardware = broadlink_provider.Sp2LrCab()


class LivingroomTv(Device):
    def __init__(self):
        self.hardware = broadlink_provider.RmPro()


class LivingroomTv(Device):
    def __init__(self):
        self.hardware = broadlink_provider.RmPro()


class Doorbell(Device):
    def __init__(self):
        self.hardware = broadlink_provider.Sp2Doorbell()


class Iron(Device):
    def __init__(self):
        self.hardware = broadlink_provider.Sp2Doorbell()

