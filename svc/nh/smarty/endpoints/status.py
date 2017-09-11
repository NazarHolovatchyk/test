from nh.smarty.endpoints.base import BaseResource
from nh.smarty import __version__ as smarty_version


class Status(BaseResource):
    def get(self):
        return self.success_response({"version": smarty_version})
