glissade_modify_schema = {
    'type': 'object',
    'required': ['arrondissement', 'nom', 'ouvert', 'deblaye'],
    'properties': {
        'arrondissement': {
            'type': 'string'
        },
        'nom': {
            'type': 'string'
        },
        'ouvert': {
            'type': 'string'
        },
        'deblaye': {
            'type': 'string'
        }
    },
    'additionalProperties': False
}
