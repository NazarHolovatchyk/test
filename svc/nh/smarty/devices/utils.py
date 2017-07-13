import time


class Delay(object):
    """
    Dummy device that waits time provided in ms parameter before returning
    """
    def send(self, cmd=0.5):
        time.sleep(seconds=cmd)
