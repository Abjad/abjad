# -*- coding: utf-8 -*-


def to_bidirectional_direction_string(argument):
    r'''Changes `argument` to bidirectional direction string.

    ..  container:: example:

        ::

            >>> stringtools.to_bidirectional_direction_string('^')
            'up'

    ..  container:: example:

        ::

            >>> stringtools.to_bidirectional_direction_string('_')
            'down'

    ..  container:: example:

        ::

            >>> stringtools.to_bidirectional_direction_string(1)
            'up'

    ..  container:: example:

        ::

            >>> stringtools.to_bidirectional_direction_string(-1)
            'down'

    Returns `argument` when `argument` is `'up'` or `'down'`.

    Returns string or none.
    '''
    lookup = {
        1: 'up',
        -1: 'down',
        Up: 'up',
        Down: 'down',
        '^': 'up',
        '_': 'down',
        'up': 'up',
        'down': 'down'
        }
    if argument in lookup:
        return lookup[argument]
    raise ValueError(argument)
