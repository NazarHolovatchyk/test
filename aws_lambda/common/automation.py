import json
import urllib2


def put(url, data):
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(url, data=json.dumps(data))
    request.add_header('Content-Type', 'application/json')
    request.get_method = lambda: 'PUT'
    try:
        response = opener.open(request)
    except urllib2.HTTPError as err:
        if err.code in [400, 501]:
            status_code = err.code
            content = err.msg
        else:
            raise
    else:
        status_code = response.code
        content = response.read()

    response_data = {}
    try:
        response_data = json.loads(content)
    except ValueError as err:
        print('Error parsing response {}: {}'.format(content, err))
    return status_code, response_data


def get(url):
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(url)
    request.get_method = lambda: 'GET'
    try:
        response = opener.open(request)
    except urllib2.HTTPError as err:
        if err.code in [400, 501]:
            status_code = err.code
            content = err.msg
        else:
            raise
    else:
        status_code = response.code
        content = response.read()

    response_data = {}
    try:
        response_data = json.loads(content)
    except ValueError as err:
        print('Error parsing response {}: {}'.format(content, err))
    return status_code, response_data


if __name__ == '__main__':
    status_code, content = get('http://home.online:5555/v1/status')
    print(status_code, content)
