import json
import logging
from datetime import datetime

from flask import request, Response
from flask_restful import Resource

logger = logging.getLogger(__name__)


class BaseResource(Resource):

    @staticmethod
    def get_param(param_name, required=True, default=None, date_format=None, is_list=False):
        if required and param_name not in request.args:
            raise ValueError("{} parameter is required".format(param_name))

        if is_list:
            param = request.args.getlist(param_name, default)
        else:
            param = request.args.get(param_name, default)

        if param is not None and date_format:
            param = datetime.strptime(param, date_format)
        return param

    @staticmethod
    def json_param(param_name, required=True, default=None, date_format=None):
        if required and param_name not in request.json:
            raise ValueError("{} parameter is required".format(param_name))
        if request.json is None:
            return default

        param = request.json.get(param_name, default)
        if param is not None and date_format:
            param = datetime.strptime(param, date_format)

        return param

    @staticmethod
    def success_response(result, status=200, headers=None,
                         content_type='application/json'):
        body = json.dumps(result)
        response = Response(body, status=status, content_type=content_type)
        if headers:
            for key, val in headers.iteritems():
                response.headers.set(key, val)
        logger.info('Success response: {} {}'.format(status, body))
        return response

    @staticmethod
    def error_response(message, status=500, headers=None,
                       content_type='application/json', details=None):
        body = ''
        if message is not None:
            content = {'error': str(message)}
            if details:
                content['details'] = str(details)
            body = json.dumps(content)
        response = Response(body, status=status, content_type=content_type)
        if headers:
            for key, val in headers.iteritems():
                response.headers.set(key, val)
        logger.info('Error response: {} {}'.format(status, body))
        return response
