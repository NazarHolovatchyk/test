def build_response(output, title='Automation', reprompt_text='', should_end_session=True, session_attributes=None,
                   small_image_url=None, large_image_url=None):
    # https://developer.amazon.com/docs/custom-skills/request-and-response-json-reference.html#response-format
    # https://developer.amazon.com/docs/custom-skills/display-interface-reference.html
    speechlet = {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': create_card(title, output, small_image_url, large_image_url),
        'shouldEndSession': should_end_session
    }

    if False:
        speechlet["directives"] = create_directives()

    if reprompt_text:
        reprompt = {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        }
        speechlet['reprompt'] = reprompt

    response = {
        'version': '1.0',
        'sessionAttributes': session_attributes or {},
        'response': speechlet
    }
    print('RESPONSE: {}'.format(response))
    return response


def create_card(title, output, small_image_url=None, large_image_url=None):
    if small_image_url and large_image_url:
        # https://developer.amazon.com/docs/custom-skills/include-a-card-in-your-skills-response.html
        # Small 720px x 480px. Large images are 1200px x 800px
        card = {
            "type": "Standard",
            "title": title,
            "text": output,
            "image": {
                "smallImageUrl": "https://smtry.net/static/img_small.png",
                "largeImageUrl": "https://smtry.net/static/img.png"
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


class BaseTemplateRenderer(object):
    BODY_TEMPLATE_1 = 'BodyTemplate1'
    BODY_TEMPLATE_2 = 'BodyTemplate2'
    BODY_TEMPLATE_3 = 'BodyTemplate3'
    BODY_TEMPLATE_6 = 'BodyTemplate6'
    LIST_TEMPLATE_1 = 'ListTemplate1'
    LIST_TEMPLATE_2 = 'ListTemplate2'

    TEMPLATE = BODY_TEMPLATE_1

    SIZE_X_SMALL = 'X_SMALL'  # 480 x 320
    SIZE_SMALL = 'SMALL'  # 720 x 480
    SIZE_MEDIUM = 'MEDIUM'  # 960 x 640
    SIZE_LARGE = 'LARGE'  # 1200 x 800
    SIZE_X_LARGE = 'X_LARGE'  # 1920 x 1280

    def __init__(self, template, title, bg_image_url='', back_button=True, token='tkn'):
        self.TEMPLATE = template
        self.title = title
        self.bg_image = self.render_image_tpl(bg_image_url, template='bg')
        self.back_button = back_button
        self.token = token

    def render(self, **kwargs):
        content = {
            "type": self.TEMPLATE,
            "token": self.token,
            "backButton": "VISIBLE" if self.back_button else "HIDDEN",
            "title": self.title,
            "backgroundImage": self.bg_image
        }
        return content

    @classmethod
    def render_image_tpl(cls, url, template, size=SIZE_LARGE):
        """
        https://developer.amazon.com/docs/custom-skills/display-interface-reference.html#image-sizes
        https://developer.amazon.com/designing-for-voice/what-alexa-says/#choose-the-right-template-on-echo-show
        BodyTemplate1:	inline images only
        List Template 1:	88 x 88
        ListTemplate2:
            Portrait (192 x 280)
            Square (280 x 280)
            4:3 (372 x 280)
            16:9 (498 x 280)
        Others: 340 x 340
        """

        if template == 'bg':
            width = 1024
            height = 600
        elif template == cls.LIST_TEMPLATE_1:
            width = 88
            height = 88
        elif template == cls.LIST_TEMPLATE_2:
            width = 280
            height = 280
        else:
            width = 340
            height = 340

        img_tpl = {
            "contentDescription": "Textured grey background",
            "sources": [
                {
                    "url": url,
                    "size": size,
                    "widthPixels": width,
                    "heightPixels": height
                }
            ]
        }
        return img_tpl

    @staticmethod
    def render_text_tpl(primary_text, secondary_text, tertiary_text):
        text_tpl = {
            "primaryText": {
                "text": primary_text,
                "type": "string"
            },
            "secondaryText": {
                "text": secondary_text,
                "type": "string"
            },
            "tertiaryText": {
                "text": tertiary_text,
                "type": "string"
            }
        }
        return text_tpl


class ListTemplateRenderer(BaseTemplateRenderer):
    def render(self, items):
        content = super(ListTemplateRenderer, self).render()
        tpl_items = []
        for item in items:
            tpl_item = {
                "token": "string",
                "image": item['image'],
                "textContent": item['text']
            }
            tpl_items.append(tpl_item)
        content["listItems"] = tpl_items
        return content


class BodyTemplateRenderer(BaseTemplateRenderer):

    def render(self, primary_text, secondary_text='', tertiary_text='', image_url=None):
        content = super(BodyTemplateRenderer, self).render()
        content["textContent"] = self.render_text_tpl(primary_text, secondary_text, tertiary_text)
        if image_url and self.TEMPLATE != self.BODY_TEMPLATE_1:
            content['image'] = self.render_image_tpl(image_url, self.TEMPLATE)
        return content


class RendererFactory(object):

    TEMPLATE_MAP = {
        BaseTemplateRenderer.BODY_TEMPLATE_1: BodyTemplateRenderer,
        BaseTemplateRenderer.BODY_TEMPLATE_2: BodyTemplateRenderer,
        BaseTemplateRenderer.BODY_TEMPLATE_3: BodyTemplateRenderer,
        BaseTemplateRenderer.BODY_TEMPLATE_6: BodyTemplateRenderer,
        BaseTemplateRenderer.LIST_TEMPLATE_1: ListTemplateRenderer,
        BaseTemplateRenderer.LIST_TEMPLATE_2: ListTemplateRenderer
    }

    @classmethod
    def get_template(cls, template, title, token='tkn', back_button=True):
        if template not in cls.TEMPLATE_MAP:
            raise ValueError('Invalid template name')
        tpl_cls = cls.TEMPLATE_MAP[template]
        tpl = tpl_cls(template=template, title=title, token=token, back_button=back_button)
        return tpl
