# -*- encoding: utf-8 -*-


def arg_to_tridirectional_direction_string(arg):
    r'''Changes `arg` to tridirectional direction string.

    ..  container:: example

        ::

            >>> stringtools.arg_to_tridirectional_direction_string('^')
            'up'

    ..  container:: example

        ::

            >>> stringtools.arg_to_tridirectional_direction_string('-')
            'center'

    ..  container:: example

        ::

            >>> stringtools.arg_to_tridirectional_direction_string('_')
            'down'

    ..  container:: example

        ::

            >>> stringtools.arg_to_tridirectional_direction_string(1)
            'up'

    ..  container:: example

        ::

            >>> stringtools.arg_to_tridirectional_direction_string(0)
            'center'

    ..  container:: example

        ::

            >>> stringtools.arg_to_tridirectional_direction_string(-1)
            'down'

    ..  container:: example

        ::

            >>> stringtools.arg_to_tridirectional_direction_string('default')
            'center'

    Returns none when `arg` is none.

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

    if arg is None:
        return None
    elif arg in lookup:
        return lookup[arg]
    raise ValueError