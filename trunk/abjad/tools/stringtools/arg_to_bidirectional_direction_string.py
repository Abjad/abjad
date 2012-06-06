def arg_to_bidirectional_direction_string(arg):
    '''Convert `arg` to bidirectional direction string:

    ::

        >>> from abjad.tools import stringtools

    ::

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

    Return str or None.
    '''

    lookup = { 
        1: 'up',
        -1: 'down',
        'up': 'up',
        'down': 'down',
        '^': 'up',
        '_': 'down',
    }

    if arg in lookup:
        return lookup[arg]
    raise ValueError
