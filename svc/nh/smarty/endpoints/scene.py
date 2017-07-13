import logging

from nh.smarty.devices.mapping import DEVICE_MAPPING
from nh.smarty.scenes.mapping import SCENES
from nh.smarty.endpoints.base import BaseResource

logger = logging.getLogger(__name__)


class SceneEndpoint(BaseResource):

    def put(self):
        try:
            scene_name = self.json_param('scene')
        except ValueError as err:
            return self.error_response(err, status=400)

        logger.info("Scene: scene={}".format(scene_name))
        if scene_name not in SCENES:
            return self.error_response('There is no scene {}'.format(scene_name), status=400)

        scene = SCENES[scene_name]
        for action in scene:
            room = action.get('room', 'house')
            device_name = action['device']
            try:
                device = DEVICE_MAPPING[room][device_name]
                logging.info('Action: {} - {}'.format(device_name, action['cmd']))
                device.send(action['cmd'])
            except ValueError as err:
                return self.error_response(str(err), status=400)
            except KeyError as err:
                return self.error_response(
                    'Error processing scene',
                    details=str(err),
                    status=501
                )
            except IOError as err:
                return self.error_response(
                    'Error sending command to a device',
                    details="Actuator command failed" + str(err),
                    status=501
                )
        return self.success_response("done")
