def arg_to_bidirectional_direction_string(arg):
    '''Convert `arg` to bidirectional direction string:

    ::

        >>> from abjad.tools import stringtools

    ::

        >>> stringtools.arg_to_bidirectional_direction_string('^')
        'up'

    ::

        >>> stringtools.arg_to_bidirectional_direction_string('_')
        Down

    ::

        >>> stringtools.arg_to_bidirectional_direction_string(1)
        'up'

    ::

        >>> stringtools.arg_to_bidirectional_direction_string(-1)
        Down

    If `arg` is 'up' or Down, `arg` will be returned.

    Return str or None.
    '''

    lookup = { 
        1: 'up',
        -1: Down,
        'up': 'up',
        Down: Down,
        '^': 'up',
        '_': Down,
    }

    if arg in lookup:
        return lookup[arg]
    raise ValueError
