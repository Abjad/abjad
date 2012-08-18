def arg_to_bidirectional_lilypond_symbol(arg):
    '''Convert `arg` to bidirectional LilyPond symbol:

    ::  

        >>> from abjad.tools import stringtools

    ::

        >>> stringtools.arg_to_tridirectional_lilypond_symbol('up')
        '^'

    ::

        >>> stringtools.arg_to_tridirectional_lilypond_symbol(Down)
        '_'

    ::

        >>> stringtools.arg_to_tridirectional_lilypond_symbol(1)
        '^'

    ::

        >>> stringtools.arg_to_tridirectional_lilypond_symbol(-1)
        '_'

    If `arg` is '^' or '_', `arg` will be returned.

    Return str or None.
    '''

    lookup = {
        1: '^',
        -1: '_',
        'up': '^',
        Down: '_',
        '^': '^',
        '_': '_',
    }

    if arg in lookup:
        return lookup[arg]
    raise ValueError
