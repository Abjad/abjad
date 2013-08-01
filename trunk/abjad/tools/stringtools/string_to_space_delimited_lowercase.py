# -*- encoding: utf-8 -*-
def string_to_space_delimited_lowercase(string):
    r'''Change uppercamelcase `string` to space-delimited lowercase:

    ::

        >>> stringtools.string_to_space_delimited_lowercase('TieSpanner')
        'tie spanner'

    Change underscore-delimited `string` to space-delimited lowercase:

    ::

        >>> stringtools.string_to_space_delimited_lowercase('tie_spanner')
        'tie spanner'

    Return space-delimited string unchanged:

    ::

        >>> stringtools.string_to_space_delimited_lowercase('tie spanner')
        'tie spanner'

    Return empty `string` unchanged:

    ::

        >>> stringtools.string_to_space_delimited_lowercase('')
        ''

    Return string.
    '''
    from abjad.tools import stringtools

    if not string:
        return string
    elif string[0].isupper():
        return stringtools.upper_camel_case_to_space_delimited_lowercase(string)
    else:
        return string.replace('_', ' ')
