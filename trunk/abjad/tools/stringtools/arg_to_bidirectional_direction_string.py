def arg_to_bidirectional_direction_string(arg):
    '''Convert `arg` to bidirectional direction string:

    ::

        >>> from abjad.tools import stringtools

    ::

        >>> stringtools.arg_to_bidirectional_direction_string('^')
        Up

    ::

        >>> stringtools.arg_to_bidirectional_direction_string('_')
        Down

    ::

        >>> stringtools.arg_to_bidirectional_direction_string(1)
        Up

    ::

        >>> stringtools.arg_to_bidirectional_direction_string(-1)
        Down

    If `arg` is Up or Down, `arg` will be returned.

    Return str or None.
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
