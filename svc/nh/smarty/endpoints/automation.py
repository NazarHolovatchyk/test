import logging

from nh.smarty.endpoints.base import BaseResource
from nh.smarty.services.broadlink_svc import BroadlinkService

logger = logging.getLogger(__name__)


class AutomationEndpoint(BaseResource):

    def put(self):
        room = self.json_param('room', required=False, default='global')
        device = self.json_param('device', required=True)
        status = self.json_param('status', required=True)

        logger.info("Automation: room={}, device={}, status={}".format(room, device, status))

        light_svc = BroadlinkService()
        try:
            light_svc.set_status(room, device, status)
        except (IOError, ValueError) as err:
            logger.error(err)
            return self.error_response("Automation command failed: {}".format(err), details=str(err), status=501)

        return self.success_response({'result': 'done'})
