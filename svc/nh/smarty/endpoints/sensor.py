import logging

from nh.smarty.devices.mapping import SENSOR_MAPPING
from nh.smarty.endpoints.base import BaseResource

logger = logging.getLogger(__name__)


class SensorEndpoint(BaseResource):

    def get(self):
        try:
            room = self.get_param('room', required=False, default='house')
            sensor = self.get_param('sensor')
        except ValueError as err:
            return self.error_response(err, status=400)

        logger.info("Sensor: room={}, sensor={}".format(room, sensor))
        room = room.replace('the ', '')
        if room not in SENSOR_MAPPING:
            return self.error_response('There is no room {}'.format(room), status=400)
        if sensor not in SENSOR_MAPPING[room]:
            return self.error_response('There is no {} sensor in {}'.format(sensor, room), status=400)

        device = SENSOR_MAPPING[room][sensor]

        try:
            result = device.value()
        except ValueError as err:
            return self.error_response(str(err), status=400)
        except IOError as err:
            return self.error_response("Error getting data from sensor", details=str(err), status=501)

        return self.success_response({'result': result})
