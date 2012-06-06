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
        'down'

    ::

        >>> stringtools.arg_to_tridirectional_direction_string(1)
        'up'

    ::

        >>> stringtools.arg_to_tridirectional_direction_string(0)
        'neutral'

    ::

        >>> stringtools.arg_to_tridirectional_direction_string(-1)
        'down'

    ::

        >>> stringtools.arg_to_tridirectional_direction_string('default')
        'neutral'

    If `arg` is None, None will be returned.

    If `arg` is 'up', 'neutral', or 'down', `arg` will be returned.

    Return str or None.
    '''

    lookup = {
        1: 'up',
        0: 'neutral',
        -1: 'down',
        'up': 'up',
        'default': 'neutral',
        'neutral': 'neutral',
        'down': 'down',
        '^': 'up',
        '-': 'neutral',
        '_': 'down',
    }

    if arg is None:
        return None
    elif arg in lookup:
        return lookup[arg]
    raise ValueError
