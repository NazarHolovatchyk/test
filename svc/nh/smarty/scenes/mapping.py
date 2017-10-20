
# {'room': '', 'device': '', 'cmd': ''}

SCENES = {
    'test': [
        {'device': 'light', 'cmd': 'off'}
    ],
    'movie': [
        {'device': 'tv', 'cmd': 'on'},
        {'device': 'delay', 'cmd': 0.5},
        {'device': 'apple', 'cmd': 'menu'},
        {'device': 'delay', 'cmd': 0.5},
        {'device': 'audio', 'cmd': 'on'},
        {'device': 'delay', 'cmd': 0.5},
        {'device': 'light', 'cmd': 'on'},
        {'device': 'delay', 'cmd': 0.5},
        {'device': 'audio', 'cmd': 'cd'},
        {'device': 'delay', 'cmd': 0.5},
        {'device': 'apple', 'cmd': 'menu'},
        {'device': 'delay', 'cmd': 0.5},
        {'device': 'apple', 'cmd': 'menu'},
        {'device': 'delay', 'cmd': 7},
        {'device': 'tv', 'cmd': 'source'},
        {'device': 'delay', 'cmd': 1},
        {'device': 'tv', 'cmd': 'up'},
        {'device': 'delay', 'cmd': 0.5},
        {'device': 'tv', 'cmd': 'right'},
        {'device': 'delay', 'cmd': 0.5},
        {'device': 'tv', 'cmd': 'right'},
        {'device': 'delay', 'cmd': 0.5},
        {'device': 'tv', 'cmd': 'right'},
        {'device': 'delay', 'cmd': 0.5},
        {'device': 'tv', 'cmd': 'ok'},
        {'device': 'delay', 'cmd': 0.5},
        {'device': 'apple', 'cmd': 'menu'}
    ],
    'finish': [
        {'device': 'tv', 'cmd': 'off'},
        {'device': 'delay', 'cmd': 0.5},
        {'device': 'audio', 'cmd': 'off'},
        {'device': 'delay', 'cmd': 0.5},
        {'device': 'apple', 'cmd': 'menu'},
        {'device': 'delay', 'cmd': 0.5},
        {'device': 'light', 'cmd': 'off'},
        {'device': 'delay', 'cmd': 0.5},
        {'device': 'apple', 'cmd': 'menu'}
    ],
    'evening': [
        {'room': 'bedroom', 'device': 'light', 'cmd': 'w5'}
    ],
    'night': [
        {'room': 'bedroom', 'device': 'light', 'cmd': 'sleep4'}
    ],
    'reset': [
        {'device': 'router', 'cmd': 'off'},
        {'device': 'delay', 'cmd': 0.5},
        {'device': 'router', 'cmd': 'on'}
    ]
}

SCENES['happy'] = SCENES['happy end']
