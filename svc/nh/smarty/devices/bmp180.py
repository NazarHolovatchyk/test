from nh.smarty.providers.bmp180 import readBmp180, mock


class BMP180(object):

    def __init__(self, sensor='temperature'):
        self.sensor = sensor
    
    def value(self):
        if self.sensor == 'pressure':
            return self.pressure()
        return self.temperature()

    @staticmethod
    def temperature():
        if mock:
            return 'NA'
        temp, _ = readBmp180()
        return round(temp, 1)

    @staticmethod
    def pressure():
        if mock:
            return 'NA'
        _, pres = readBmp180()
        return round(pres, 0)
