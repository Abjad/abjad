# -*- encoding: utf-8 -*-


def arg_to_bidirectional_lilypond_symbol(arg):
    r'''Convert `arg` to bidirectional LilyPond symbol:

        >>> stringtools.arg_to_tridirectional_lilypond_symbol(Up)
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

    Returns str or None.
    '''

    lookup = {
        1: '^',
        -1: '_',
        Up: '^',
        Down: '_',
        'up': '^',
        'down': '_',
        '^': '^',
        '_': '_',
    }

    if arg in lookup:
        return lookup[arg]
    raise ValueError
