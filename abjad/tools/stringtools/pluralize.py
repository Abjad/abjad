# -*- encoding: utf-8 -*-


def pluralize(string, count=None):
    r'''Pluralize English `string`. Change terminal `-y` to `-ies`:

    ::

        >>> stringtools.pluralize('catenary')
        'catenaries'

    Add `-es` to terminal `-s`, `-sh`, `-x` and `-z`:

    ::

        >>> stringtools.pluralize('brush')
        'brushes'

    Add `-s` to all other strings:

    ::

        >>> stringtools.pluralize('shape')
        'shapes'

    Returns string.
    '''
    if count == 1:
        return string
    if string.endswith('y'):
        return string[:-1] + 'ies'
    elif string.endswith(('s', 'sh', 'x', 'z')):
        return string + 'es'
    else:
        return string + 's'