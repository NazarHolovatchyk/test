import json
import os


def get_context(event=None):
    context_filename = os.environ.get('LAMBDA_CONTEXT', '.context')

    if event is None:
        event = {}

    context = {}
    if os.path.isfile(context_filename):
        with open(context_filename, 'r') as f:
            context = json.loads(f.read())

    # context.update(os.environ)
    context.update(event)
    return context
