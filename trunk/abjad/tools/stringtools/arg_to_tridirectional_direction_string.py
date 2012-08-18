def arg_to_tridirectional_direction_string(arg):
    '''Convert `arg` to tridirectional direction string:

    ::  

        >>> from abjad.tools import stringtools

    ::

        >>> stringtools.arg_to_tridirectional_direction_string('^')
        Up

    ::

        >>> stringtools.arg_to_tridirectional_direction_string('-')
        'neutral'

    ::

        >>> stringtools.arg_to_tridirectional_direction_string('_')
        Down

    ::

        >>> stringtools.arg_to_tridirectional_direction_string(1)
        Up

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

    If `arg` is Up, 'neutral', or Down, `arg` will be returned.

    Return str or None.
    '''

    lookup = {
        1: Up,
        0: 'neutral',
        -1: Down,
        Up: Up,
        'default': 'neutral',
        'neutral': 'neutral',
        Down: Down,
        '^': Up,
        '-': 'neutral',
        '_': Down,
    }

    if arg is None:
        return None
    elif arg in lookup:
        return lookup[arg]
    raise ValueError
