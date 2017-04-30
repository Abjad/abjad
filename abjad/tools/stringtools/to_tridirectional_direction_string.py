# -*- coding: utf-8 -*-


def to_tridirectional_direction_string(argument):
    r'''Changes `argument` to tridirectional direction string.

    ..  container:: example

        ::

            >>> stringtools.to_tridirectional_direction_string('^')
            'up'

    ..  container:: example

        ::

            >>> stringtools.to_tridirectional_direction_string('-')
            'center'

    ..  container:: example

        ::

            >>> stringtools.to_tridirectional_direction_string('_')
            'down'

    ..  container:: example

        ::

            >>> stringtools.to_tridirectional_direction_string(1)
            'up'

    ..  container:: example

        ::

            >>> stringtools.to_tridirectional_direction_string(0)
            'center'

    ..  container:: example

        ::

            >>> stringtools.to_tridirectional_direction_string(-1)
            'down'

    ..  container:: example

        ::

            >>> stringtools.to_tridirectional_direction_string('default')
            'center'

    Returns none when `argument` is none.

    Returns string or none.
    '''
    lookup = {
        Up: 'up',
        '^': 'up',
        'up': 'up',
        1: 'up',
        Down: 'down',
        '_': 'down',
        'down': 'down',
        -1: 'down',
        Center: 'center',
        '-': 'center',
        0: 'center',
        'center': 'center',
        'default': 'center',
        'neutral': 'center',
        }
    if argument is None:
        return None
    elif argument in lookup:
        return lookup[argument]
    raise ValueError(argument)
