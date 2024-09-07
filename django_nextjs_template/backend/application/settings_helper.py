import os

def config_get(key: str, **kwargs: str | bool | None) -> str | bool | None:
    value = os.environ.get(key)
    if value is None or value == '':
        if 'default' in kwargs:
            value = kwargs['default']
        else:
            raise ValueError(f'No environment var {key}')
    return value
