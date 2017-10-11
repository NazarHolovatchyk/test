import logging

from nh.smarty.devices.mapping import DEVICE_MAPPING
from nh.smarty.endpoints.base import BaseResource

logger = logging.getLogger(__name__)


class ActuatorEndpoint(BaseResource):

    def put(self):
        try:
            room = self.json_param('room', required=False, default='house')
            device_name = self.json_param('device', required=True)
            cmd = self.json_param('cmd', required=True)
        except ValueError as err:
            return self.error_response(err, status=400)

        logger.info("Actuator: room={}, device={}, command={}".format(room, device_name, cmd))
        room = room.replace('the ', '')
        if room not in DEVICE_MAPPING:
            return self.error_response('There is no room: {}'.format(room), status=400)

        if device_name not in DEVICE_MAPPING[room]:
            return self.error_response('There is no {} device in {}'.format(device_name, room), status=400)

        device = DEVICE_MAPPING[room][device_name]

        try:
            device.send(cmd)
        except ValueError as err:
            return self.error_response(str(err), status=400)
        except IOError as err:
            return self.error_response(
                'Error sending command to the device',
                details="Actuator command failed" + str(err),
                status=501
            )

        return self.success_response({'result': 'done'})
