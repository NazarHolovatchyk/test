import argparse
import json

from nh.smarty.app import setup_app
app = setup_app()


def get_briefing(briefing_name):
    if briefing_name == 'weather':
        from nh.smarty.providers.openweathermap import OWMBriefing
        api_key = app.config['OPEN_WEATHER_MAP_API_KEY']
        return OWMBriefing(api_key)
    raise ValueError('Unknown briefing')


if __name__ == '__main__':
    parser = argparse.ArgumentParser('python briefing_cli.py', description='Briefing CLI')
    parser.add_argument("-n", "--name", dest="name", help="Briefing name")
    parser.add_argument("-o", "--output_path", dest="output_path", default='/tmp/briefing.txt', help="Full output path")
    parsed = parser.parse_args()

    briefing = get_briefing(parsed.name)
    data = briefing.get_data()

    with open(parsed.output_path, 'w') as f:
        f.write(json.dumps(data))
