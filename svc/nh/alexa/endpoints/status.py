from nh.alexa.endpoints.base import BaseResource
from nh.alexa import __version__ as package_version


class Status(BaseResource):
    def get(self):
        return self.success_response({"version": package_version})
