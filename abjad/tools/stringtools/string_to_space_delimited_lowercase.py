# -*- encoding: utf-8 -*-


def string_to_space_delimited_lowercase(string):
    r'''Change uppercamelcase `string` to space-delimited lowercase:

    ::

        >>> stringtools.string_to_space_delimited_lowercase('LogicalTie')
        'logical tie'

    Change underscore-delimited `string` to space-delimited lowercase:

    ::

        >>> stringtools.string_to_space_delimited_lowercase('tie_chain')
        'tie chain'

    Returns space-delimited string unchanged:

    ::

        >>> stringtools.string_to_space_delimited_lowercase('tie chain')
        'tie chain'

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
