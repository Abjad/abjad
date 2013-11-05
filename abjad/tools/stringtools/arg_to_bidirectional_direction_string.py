# -*- encoding: utf-8 -*-


def arg_to_bidirectional_direction_string(arg):
    r'''Convert `arg` to bidirectional direction string:

        >>> stringtools.arg_to_bidirectional_direction_string('^')
        'up'

    ::

        >>> stringtools.arg_to_bidirectional_direction_string('_')
        'down'

    ::

        >>> stringtools.arg_to_bidirectional_direction_string(1)
        'up'

    ::

        >>> stringtools.arg_to_bidirectional_direction_string(-1)
        'down'

    If `arg` is 'up' or 'down', `arg` will be returned.

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
