SPEECH_TYPE_TEXT = 'PlainText'
SPEECH_TYPE_SSML = 'SSML'


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
        self.bg_image = self.render_image_tpl(bg_image_url, custom_template='bg')
        self.back_button = back_button
        self.token = token

    def render(self, **kwargs):
        content = {
            "type": self.TEMPLATE,
            "token": self.token,
            "backButton": "VISIBLE" if self.back_button else "HIDDEN",
            "title": self.title
        }
        if self.bg_image:
            content["backgroundImage"] = self.bg_image
        return content

    def render_image_tpl(self, url, description=None, custom_template=None, size=SIZE_LARGE):
        """
        https://developer.amazon.com/docs/custom-skills/display-interface-reference.html#image-sizes
        https://developer.amazon.com/designing-for-voice/what-alexa-says/#choose-the-right-template-on-echo-show
        BodyTemplate1:	inline images only
        List Template 1:	88 x 88
        ListTemplate2:
            Portrait (192 x 280)
          * Square (280 x 280)
            4:3 (372 x 280)
            16:9 (498 x 280)
        Others: 340 x 340
        """
        if not url:
            return None

        template = custom_template or self.TEMPLATE

        if template == 'bg':
            width = 1024
            height = 600
        elif template == self.LIST_TEMPLATE_1:
            width = 88
            height = 88
        elif template == self.LIST_TEMPLATE_2:
            width = 280
            height = 280
        else:
            width = 340
            height = 340

        img_tpl = {
            "contentDescription": description or "image description",
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
    def render_text_tpl(primary_text, secondary_text='', tertiary_text='', speech_type=SPEECH_TYPE_TEXT, **kwargs):
        text_tpl = {
            "primaryText": {
                "text": primary_text,
                "type": speech_type
            },
            "secondaryText": {
                "text": secondary_text,
                "type": speech_type
            },
            "tertiaryText": {
                "text": tertiary_text,
                "type": speech_type
            }
        }
        return text_tpl


class ListTemplateRenderer(BaseTemplateRenderer):
    def render(self, items):
        """
        item: {
            'primary_text': 'Item 1',
            'secondary_text': 'secondary text goes here',
            'tertiary_text': 'my tertiary text',
            'image': 'https://aws/my_bkt/img1.jpg'
        }
        :param items: [item]
        :return: template string
        """
        content = super(ListTemplateRenderer, self).render()
        tpl_items = []
        for item in items:
            tpl_item = {
                "token": item.get('token', 'tkn1'),
                "image": self.render_image_tpl(item['image']),
                "textContent": self.render_text_tpl(**item)
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


if __name__ == '__main__':
    renderer = RendererFactory.get_template(
        BaseTemplateRenderer.LIST_TEMPLATE_2,
        'My list'
    )
    items = [
        {
            'primary_text': 'Item 1',
            'secondary_text': 'secondary text goes here',
            'tertiary_text': 'my tertiary text',
            'image': 'https://aws/my_bkt/img1.jpg'
        },
        {
            'primary_text': 'Item 2',
            'secondary_text': 'secondary text goes here',
            'tertiary_text': 'my tertiary text',
            'image': 'https://aws/my_bkt/img2.jpg'
        },

    ]
    resp = renderer.render(items)
    print(resp)
