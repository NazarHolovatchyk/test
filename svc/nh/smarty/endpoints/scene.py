import logging

from nh.smarty.endpoints.base import BaseResource
from nh.smarty.services.broadlink_svc import BroadlinkService, ServiceError

logger = logging.getLogger(__name__)


class SceneEndpoint(BaseResource):

    def put(self):
        return self.error_response("Not implemented", status=501)
