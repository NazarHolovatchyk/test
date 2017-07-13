"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""
from __future__ import print_function

import json
import urllib
import urllib2

from common.context import get_context


def build_response(output, title='Automation', reprompt_text='', should_end_session=True, session_attributes=None):
    speechlet = {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }
    response = {
        'version': '1.0',
        'sessionAttributes': session_attributes or {},
        'response': speechlet
    }
    print('RESPONSE: {}'.format(response))
    return response


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


def get(url, params=None):
    if params:
        param_str = urllib.urlencode(params)
        url += '?' + param_str
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


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could add those here"""
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa Skills Kit sample"
    return build_response(speech_output, card_title, should_end_session=False)


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "bay"
    return build_response(speech_output, card_title)


def create_favorite_color_attributes(favorite_color):
    return {"favoriteColor": favorite_color}


def set_color_in_session(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the user."""
    card_title = intent['name']
    session_attributes = {}
    if 'Color' in intent['slots']:
        favorite_color = intent['slots']['Color']['value']
        session_attributes = create_favorite_color_attributes(favorite_color)
        speech_output = "I now know your favorite color is " + \
                        favorite_color + \
                        ". You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
        reprompt_text = "You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your favorite color is. " \
                        "You can tell me your favorite color by saying, " \
                        "my favorite color is red."
    return build_response(speech_output, card_title, reprompt_text, should_end_session=False,
                          session_attributes=session_attributes)


def get_color_from_session(intent, session):
    if session.get('attributes', {}) and "favoriteColor" in session.get('attributes', {}):
        favorite_color = session['attributes']['favoriteColor']
        speech_output = "Your favorite color is " + favorite_color + ". Goodbye."
        should_end_session = True
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "You can say, my favorite color is red."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(speech_output, title=intent['name'], should_end_session=should_end_session)


def actuator_intent(intent, session):
    print("intent: {}, session: {}".format(intent, session))
    # "OnOffIntent", "DimmLightIntent", "AutomationIntent"
    context = get_context()
    url = context.get('AutomationServiceUrl')
    uri = url + '/v1/actuator'

    slots = intent.get('slots', {})
    room = slots['room'].get('value', 'house')
    if intent['name'] == "DimmLightIntent":
        device = 'light'
        state = slots['intelite_state'].get('value')
        map = {
            'on': 'on',
            'off': 'off',
            'maximum': 'max',
            'level one': 'w1',
            'level two': 'w2',
            'level five': 'w5',
            'level eight': 'w8',
            'level ten': 'w10',
            'sleep one': 'sleep1',
            'sleep two': 'sleep2',
            'sleep three': 'sleep3',
            'sleep four': 'sleep4',
            'level 1': 'w1',
            'level 2': 'w2',
            'level 5': 'w5',
            'level 8': 'w8',
            'level 10': 'w10',
            'sleep 1': 'sleep1',
            'sleep 2': 'sleep2',
            'sleep 3': 'sleep3',
            'sleep 4': 'sleep4'
        }
        if state not in map:
            return build_response('Unexpected state {}'.format(state), title=intent['name'])
        status = map[state]
    elif intent['name'] == "OnOffIntent":
        device = slots['device']['value'].replace('the ', '')
        status = '1' if slots['on_off_state'].get('value') == 'on' else '0'
    else:
        device = slots['device']['value']
        status = slots['status'].get('value')
    data = {
        'room': room,
        'device': device,
        'cmd': status
    }
    print('Request PUT: {} data={}'.format(uri, data))

    status_code, response_data = put(uri, data=data)
    print('Actuator response: {} - {}'.format(status_code, response_data))

    if status_code == 200:
        speech_output = 'done'
    elif status_code in [400, 501]:
        speech_output = response_data.get('error', 'error')
    else:
        speech_output = 'error'
    return build_response(speech_output, title=intent['name'])


def sensor_intent(intent, session):
    print("Sensor intent: {}, session: {}".format(intent, session))
    context = get_context()
    url = context.get('AutomationServiceUrl')
    uri = url + '/v1/sensor'

    slots = intent.get('slots', {})
    room = slots.get('room', {}).get('value', 'house')
    sensor = slots['sensor'].get('value')
    params = {
        'room': room,
        'sensor': sensor
    }
    print('Request GET: {} params={}'.format(uri, params))

    status_code, response_data = get(uri, params=params)
    print('Service response: {} - {}'.format(status_code, response_data))

    if status_code == 200:
        speech_output = response_data['result']
    elif status_code in [400, 501]:
        speech_output = response_data.get('error', 'error')
    else:
        speech_output = 'error'
    return build_response(speech_output, title='{} {}'.format(room, sensor))


def scene_intent(intent, session):
    print("scene_intent: {}, session: {}".format(intent, session))

    context = get_context()
    url = context.get('AutomationServiceUrl')
    uri = url + '/v1/scene'

    slots = intent.get('slots', {})
    scene = slots['scene'].get('value')
    data = {
        'scene': scene
    }
    print('Request PUT: {} data={}'.format(uri, data))

    status_code, response_data = put(uri, data=data)
    print('Scene response: {} - {}'.format(status_code, response_data))

    if status_code == 200:
        speech_output = '{} scene activated'.format(scene)
    elif status_code in [400, 501]:
        speech_output = response_data.get('error', 'error')
    else:
        speech_output = 'error'
    return build_response(speech_output, title='Scene')


def version_intent(intent, session):
    print("version_intent: {}, session: {}".format(intent, session))
    context = get_context()
    url = context.get('AutomationServiceUrl')
    uri = url + '/v1/status'
    print('Request GET: {}'.format(uri))

    status_code, content = get(uri)
    print('Automation service response: {} - {}'.format(status_code, content))

    # response = requests.get(uri)
    # print('Automation service response: {} - {}'.format(response.status_code, response.content))
    # if response.status_code != 200:
    if status_code != 200:
        speech_output = 'Error calling Automation service'
    else:
        # data = response.json()
        data = json.loads(content)
        version = data['version']
        speech_output = 'Automation service version is {}'.format(version)
    return build_response(speech_output, title=intent['name'])


# --------------- Events ------------------
def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """
    Called when the user launches the skill without specifying what they want
    """
    print("on_launch request={}, session={}".format(launch_request, session))
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("ON INTENT: request={}, session={}".format(intent_request, session))

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name in ["OnOffIntent", "DimmLightIntent", "AutomationIntent"]:
        return actuator_intent(intent, session)
    if intent_name == "SceneIntent":
        return scene_intent(intent, session)
    if intent_name == "SensorIntent":
        return sensor_intent(intent, session)
    if intent_name == "VersionIntent":
        return version_intent(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------
def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print('Event: {}'.format(event))
    print("event.session.application.applicationId=" + event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


if __name__ == '__main__':
    event = {
        "session": {
            "new": False,
            "application": {
                "applicationId": "test"
            }
        },
        "request": {
            "requestId": "test",
            "type": "IntentRequest",
            "intent": {
                # "name": "VersionIntent"
                "name": "DimmLightIntent",
                'slots': {
                    'room': {
                        'value': 'bedroom'
                    },
                    'intelite_state': {
                        'value': 'sleep one'
                    }
                }
            }
        }
    }
    lambda_handler(event, None)
