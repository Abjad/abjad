# -*- encoding: utf-8 -*-


def string_to_space_delimited_lowercase(string):
    r'''Change uppercamelcase `string` to space-delimited lowercase:

    ::

        >>> stringtools.string_to_space_delimited_lowercase('LogicalTie')
        'logical tie'

    Change underscore-delimited `string` to space-delimited lowercase:

    ::

        >>> stringtools.string_to_space_delimited_lowercase('logical_tie')
        'logical tie'

    Returns space-delimited string unchanged:

    ::

        >>> stringtools.string_to_space_delimited_lowercase('logical tie')
        'logical tie'

    Returns empty `string` unchanged:

    ::

        >>> stringtools.string_to_space_delimited_lowercase('')
        ''

    Returns string.
    '''
    from abjad.tools import stringtools

    if not string:
        return string
    elif string[0].isupper():
        return stringtools.upper_camel_case_to_space_delimited_lowercase(string)
    else:
        return string.replace('_', ' ')
