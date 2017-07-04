
def build_speechlet_response(output, title='Automation', reprompt_text='', should_end_session=True):
    return {
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


def build_response(speechlet_response, session_attributes=None):
    response = {
        'version': '1.0',
        'sessionAttributes': session_attributes or {},
        'response': speechlet_response
    }
    print('RESPONSE: {}'.format(response))
    return response
