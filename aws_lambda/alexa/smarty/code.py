"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""
from __future__ import print_function

from common.alexa import build_response
from common.context import get_context
from common.http import get, put
from common.intelite import INTELITE_MAP


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could add those here"""
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa Skills Kit sample"
    return build_response(speech_output, card_title, should_end_session=False)


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "bay"
    return build_response(speech_output, card_title)


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
        if state not in INTELITE_MAP:
            return build_response('Unexpected state {}'.format(state), title=intent['name'])
        status = INTELITE_MAP[state]
    elif intent['name'] == "OnOffIntent":
        device = slots['device']['value'].replace('the ', '')
        status = 'on' if slots['on_off_state'].get('value') == 'on' else 'off'
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


def weather_intent(intent, session):
    print("weather_intent: {}, session: {}".format(intent, session))

    context = get_context()
    url = context.get('AutomationServiceUrl')
    uri = url + '/v1/weather'

    slots = intent.get('slots', {})
    day = slots.get('day', {}).get('value', '')
    data = {'day': day}
    print('Request GET: {} data={}'.format(uri, data))

    status_code, response_data = get(uri, data=data)
    print('Scene response: {} - {}'.format(status_code, response_data))

    if status_code == 200:
        speech_output = 'On {} is {}'.format(response_data[0]['title'], response_data[0]['text'])
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

    status_code, response_data = get(uri)
    print('Automation service response: {} - {}'.format(status_code, response_data))

    # response = requests.get(uri)
    # print('Automation service response: {} - {}'.format(response.status_code, response.content))
    # if response.status_code != 200:
    if status_code != 200:
        speech_output = 'Error calling Automation service'
    else:
        version = response_data['version']
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
    if intent_name == "WeatherIntent":
        return weather_intent(intent, session)
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
    # "AutomationServiceUrl": "https://smrty.net"
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
                # "name": "DimmLightIntent",
                "name": "OnOffIntent",
                "slots": {
                    "room": {
                        "value": "house"
                    },
                    "device": {
                        "value": "light"
                    },
                    "on_off_state": {
                        "value": "on"
                    }
                }
            }
        }
    }
    lambda_handler(event, None)
