from datetime import datetime
from uuid import uuid4


class BaseBriefing(object):

    def get_data(self):
        raise NotImplemented

    @staticmethod
    def create_briefing_item(title, text, stream_url=None, read_more_link=None):
        item = {
            'uid': str(uuid4()),
            'updateDate': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.0Z'),
            'titleText': title,
            'mainText': text,
            'streamUrl': '',
            'redirectionURL': 'https://smrty.net/v1/briefing/weather'
        }
        if stream_url:
            item['streamUrl'] = stream_url
        if read_more_link:
            item['redirectionURL'] = read_more_link
        return item
