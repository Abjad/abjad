# -*- encoding: utf-8 -*-


def to_space_delimited_lowercase(string):
    r'''Changes `string` to space-delimited lowercase.
    
    ..  container:: example

        Changes upper camel case `string` to space-delimited lowercase:

        ::

            >>> stringtools.to_space_delimited_lowercase('LogicalTie')
            'logical tie'

    ..  container:: example

        Changes underscore-delimited `string` to space-delimited lowercase:

        ::

            >>> stringtools.to_space_delimited_lowercase('logical_tie')
            'logical tie'

    ..  container:: example

        Returns space-delimited string unchanged:

        ::

            >>> stringtools.to_space_delimited_lowercase('logical tie')
            'logical tie'

    ..  container:: example

        Returns empty `string` unchanged:

        ::

            >>> stringtools.to_space_delimited_lowercase('')
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