
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
