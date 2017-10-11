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
    # https://developer.amazon.com/docs/custom-skills/include-a-card-in-your-skills-response.html
    # card = {
    #     "type": "Standard",
    #     "title": title,
    #     "text": output,
    #     "image": {
    #         "smallImageUrl": "https://smtry.net/static/img_small.png",
    #         "largeImageUrl": "https://smtry.net/static/img.png"
    #     }
    # }
    # speechlet['card'] = card
    response = {
        'version': '1.0',
        'sessionAttributes': session_attributes or {},
        'response': speechlet
    }
    print('RESPONSE: {}'.format(response))
    return response
