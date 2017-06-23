import logging

from nh.alexa.endpoints.base import BaseResource
from nh.alexa.services.broadlink_svc import BroadlinkService, ServiceError

logger = logging.getLogger(__name__)


class AutomationEndpoint(BaseResource):

    def put(self):
        room = self.json_param('room', required=False, default='livingroom')
        device = self.json_param('device', required=True)
        status = self.json_param('status', required=True)

        logger.info("Automation: room={}, device={}, status={}".format(room, device, status))

        light_svc = BroadlinkService()
        try:
            light_svc.set_status(room, device, status)
        except ServiceError as err:
            logger.error(err)
            return self.error_response("Failed to change light state", details=str(err), status=501)

        return self.success_response({'result': 'done'})
