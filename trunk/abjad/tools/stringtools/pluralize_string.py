# -*- encoding: utf-8 -*-
def pluralize_string(string):
    r'''.. versionadded:: 2.13

    Pluralize English `string`. Change terminal `-y` to `-ies`:

    ::

        >>> stringtools.pluralize_string('catenary')
        'catenaries'

    Add `-es` to terminal `-s`, `-sh`, `-x` and `-z`:

    ::

        >>> stringtools.pluralize_string('brush')
        'brushes'

    Add `-s` to all other strings:

    ::

        >>> stringtools.pluralize_string('shape')
        'shapes'

    Return string.
    '''
    if string.endswith('y'):
        return string[:-1] + 'ies'
    elif string.endswith(('s', 'sh', 'x', 'z')):
        return string + 'es'
    else:
        return string + 's'
