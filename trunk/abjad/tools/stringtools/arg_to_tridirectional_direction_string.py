def arg_to_tridirectional_direction_string(arg):
    '''Convert `arg` to tridirectional direction string:

    ::  

        >>> from abjad.tools import stringtools

    ::

        >>> stringtools.arg_to_tridirectional_direction_string('^')
        'up'

    ::

        >>> stringtools.arg_to_tridirectional_direction_string('-')
        'neutral'

    ::

        >>> stringtools.arg_to_tridirectional_direction_string('_')
        Down

    ::

        >>> stringtools.arg_to_tridirectional_direction_string(1)
        'up'

    ::

        >>> stringtools.arg_to_tridirectional_direction_string(0)
        'neutral'

    ::

        >>> stringtools.arg_to_tridirectional_direction_string(-1)
        Down

    ::

        >>> stringtools.arg_to_tridirectional_direction_string('default')
        'neutral'

    If `arg` is None, None will be returned.

    If `arg` is 'up', 'neutral', or Down, `arg` will be returned.

    Return str or None.
    '''

    lookup = {
        1: 'up',
        0: 'neutral',
        -1: Down,
        'up': 'up',
        'default': 'neutral',
        'neutral': 'neutral',
        Down: Down,
        '^': 'up',
        '-': 'neutral',
        '_': Down,
    }

    if arg is None:
        return None
    elif arg in lookup:
        return lookup[arg]
    raise ValueError
