# -*- encoding: utf-8 -*-


def arg_to_bidirectional_direction_string(arg):
    r'''Changes `arg` to bidirectional direction string.

    ..  container:: example:

        ::

            >>> stringtools.arg_to_bidirectional_direction_string('^')
            'up'

    ..  container:: example:

        ::

            >>> stringtools.arg_to_bidirectional_direction_string('_')
            'down'

    ..  container:: example:

        ::

            >>> stringtools.arg_to_bidirectional_direction_string(1)
            'up'

    ..  container:: example:

        ::

            >>> stringtools.arg_to_bidirectional_direction_string(-1)
            'down'

    Returns `arg` when `arg` is `'up'` or `'down'`.

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

    if arg in lookup:
        return lookup[arg]
    raise ValueError