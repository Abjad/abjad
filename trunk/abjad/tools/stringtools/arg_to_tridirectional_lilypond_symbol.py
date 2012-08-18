def arg_to_tridirectional_lilypond_symbol(arg):
    '''Convert `arg` to tridirectional LilyPond symbol:

    ::  

        >>> from abjad.tools import stringtools

    ::

        >>> stringtools.arg_to_tridirectional_lilypond_symbol('up')
        '^'

    ::

        >>> stringtools.arg_to_tridirectional_lilypond_symbol('neutral')
        '-'

    ::

        >>> stringtools.arg_to_tridirectional_lilypond_symbol('default')
        '-'

    ::

        >>> stringtools.arg_to_tridirectional_lilypond_symbol(Down)
        '_'

    ::

        >>> stringtools.arg_to_tridirectional_lilypond_symbol(1)
        '^'

    ::

        >>> stringtools.arg_to_tridirectional_lilypond_symbol(0)
        '-'

    ::

        >>> stringtools.arg_to_tridirectional_lilypond_symbol(-1)
        '_'

    If `arg` is None, None will be returned.

    If `arg` is '^', '-', or '_', `arg` will be returned.

    Return string or None.
    '''

    lookup = {
        Up: '^',
        Down: '_',
        1: '^',
        0: '-',
        -1: '_',
        'up': '^',
        'neutral': '-',
        'default': '-',
        'down': '_',
        '^': '^',
        '-': '-',
        '_': '_',
    }

    if arg is None:
        return None 
    elif arg in lookup:
        return lookup[arg]
    raise ValueError
