def arg_to_tridirectional_direction_string(arg):
    '''Convert `arg` to tridirectional direction string:

    ::  

        >>> from abjad.tools import stringtools

    ::

        >>> stringtools.arg_to_tridirectional_direction_string('^')
        'up'

    ::

        >>> stringtools.arg_to_tridirectional_direction_string('-')
        'center'

    ::

        >>> stringtools.arg_to_tridirectional_direction_string('_')
        'down'

    ::

        >>> stringtools.arg_to_tridirectional_direction_string(1)
        'up'

    ::

        >>> stringtools.arg_to_tridirectional_direction_string(0)
        'center'

    ::

        >>> stringtools.arg_to_tridirectional_direction_string(-1)
        'down'

    ::

        >>> stringtools.arg_to_tridirectional_direction_string('default')
        'center'

    If `arg` is None, None will be returned.

    Return str or None.
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
