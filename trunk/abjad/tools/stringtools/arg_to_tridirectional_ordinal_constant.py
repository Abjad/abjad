def arg_to_tridirectional_ordinal_constant(arg):
    '''Convert `arg` to tridirectional ordinal constant:

    ::

        >>> from abjad.tools import stringtools

    ::

        >>> stringtools.arg_to_tridirectional_ordinal_constant('^')
        Up

    ::

        >>> stringtools.arg_to_tridirectional_ordinal_constant('_')
        Down

    ::

        >>> stringtools.arg_to_tridirectional_ordinal_constant(1)
        Up

    ::

        >>> stringtools.arg_to_tridirectional_ordinal_constant(-1)
        Down

    If `arg` is Up, Center or Down, `arg` will be returned.

    Return OrdinalConstant or None.
    '''

    lookup = {
        Up: Up,
        '^': Up,
        'up': Up,
        1: Up,
        Down: Down,
        '_': Down,
        'down': Down,
        -1: Down,
        Center: Center,
        '-': Center,
        0: Center,
        'center': Center,
        'default': Center,
        'neutral': Center,
    }
    if arg is None:
        return None
    elif arg in lookup:
        return lookup[arg]
    raise ValueError

