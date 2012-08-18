def arg_to_tridirectional_lilypond_symbol(arg):
    '''Convert `arg` to tridirectional LilyPond symbol:

    ::  

        >>> from abjad.tools import stringtools

    ::

        >>> stringtools.arg_to_tridirectional_lilypond_symbol(Up)
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
        '^': '^',
        'up': '^',
        1: '^',
        Down: '_',
        '_': '_',
        'down': '_',
        -1: '_',
        Center: '-',
        '-': '-',
        0: '-',
        'center': '-',
        'default': '-',
        'neutral': '-',
    }

    if arg is None:
        return None 
    elif arg in lookup:
        return lookup[arg]
    raise ValueError
