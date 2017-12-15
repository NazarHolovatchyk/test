SPEECH_TYPE_TEXT = 'PlainText'
SPEECH_TYPE_SSML = 'SSML'


def build_response(output, title='Automation', reprompt_text='', should_end_session=True, session_attributes=None,
                   list_items=None, bg_img_url=None, use_card=True, use_ssml=False):
    # https://developer.amazon.com/docs/custom-skills/request-and-response-json-reference.html#response-format
    # https://developer.amazon.com/docs/custom-skills/display-interface-reference.html
    speech_type = SPEECH_TYPE_SSML if use_ssml else SPEECH_TYPE_TEXT
    speech_key = 'ssml' if use_ssml else 'text'
    speechlet = {
        'outputSpeech': {
            'type': speech_type,
            speech_key: output
        },
        'shouldEndSession': should_end_session
    }

    if use_card:
        speechlet['card'] = create_card(title, output, bg_img_url)

    if reprompt_text:
        reprompt = {
            'outputSpeech': {
                'type': speech_type,
                'text': reprompt_text
            }
        }
        speechlet['reprompt'] = reprompt

    if list_items:
        speechlet["directives"] = [
            {
                "type": "Display.RenderTemplate",
                "template": render_list_template(title, list_items, bg_image_url=bg_img_url)
            }
        ]
    response = {
        'version': '1.0',
        'sessionAttributes': session_attributes or {},
        'response': speechlet
    }

    print('RESPONSE: {}'.format(response))
    return response


def create_card(title, output, bg_image_url=None):
    # https://developer.amazon.com/docs/custom-skills/include-a-card-in-your-skills-response.html
    # Small 720px x 480px. Large images are 1200px x 800px
    if not bg_image_url:
        card = {
            'type': 'Standard',
            'title': title,
            'text': output,
            'image': {
                "smallImageUrl": bg_image_url,
                "largeImageUrl": bg_image_url
            }
        }
    else:
        card = {
            'type': 'Simple',
            'title': title,
            'content': output
        }
    return card


def create_directives():
    template = ''
    directives = [
        {
            "type": "Display.RenderTemplate",
            "template": template
        }
    ]
    return directives


def render_list_template(title, list_items, back_btn=True, bg_image_url=None, token='tkn1', template="ListTemplate1"):
    response = {
        "type": template,
        "token": token,
        "backButton": "VISIBLE" if back_btn else "HIDDEN",
        "title": title
    }
    if bg_image_url:
        response["image"] = {
            # "smallImageUrl": "https://carfu.com/resources/card-images/race-car-small.png",
            "largeImageUrl": bg_image_url
        }
        # render_image({"url": bg_image_url})
    rendered_list = []
    for item in list_items:
        rendered_item = {
            "token": item.get('token', 'tkn1'),
            # "image": render_image(item, template=template),
            "textContent": render_text_item(**item)
        }

        rendered_list.append(rendered_item)
    response['listItems'] = rendered_list
    return response


def render_text_item(primary_text='', secondary_text='', tertiary_text='', speech_type=SPEECH_TYPE_TEXT, **kwargs):
    speech_key = 'ssml' if speech_type == SPEECH_TYPE_SSML else 'text'
    text_tpl = {
        "primaryText": {
            speech_key: primary_text,
            "type": speech_type
        }
    }
    if secondary_text:
        text_tpl["secondaryText"] = {
            speech_key: secondary_text,
            "type": speech_type
        }
    if tertiary_text:
        text_tpl["tertiaryText"] = {
            speech_key: tertiary_text,
            "type": speech_type
        }
    return text_tpl


def render_image(img, template='bg'):
    # if template == 'ListTemplate1':
    #     width = 88
    #     height = 88
    # else:
    #     width = 1024
    #     height = 600
    image = {
        "contentDescription": img.get('description', 'image'),
        "sources": [
            {
                "url": img["url"],
                # "widthPixels": width,
                # "heightPixels": height,
                # "size": "LARGE"
            }
        ]
    }
    return image
