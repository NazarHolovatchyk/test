import logging
import platform

from nh.smarty.endpoints.base import BaseResource
from svc.nh.smarty.utils.cmd import exec_command

logger = logging.getLogger(__name__)


class SystemEndpoint(BaseResource):

    def get(self, device):

        logger.info("System: {}".format(device))

        if device not in ['disk']:
            return self.error_response("Unknown system device: {}".format(device), status=400)

        if platform.system() == 'Darwin':
            cmd = "df -h | grep disk1 | awk '{print $5}'"
        else:
            cmd = "df -h | grep root | awk '{print $5}'"

        try:
            output, _ = exec_command(cmd)
        except IOError as err:
            logger.error(err)
            return self.error_response("Internal error", status=501)

        return self.success_response({'result': output.strip()})
