# -*- encoding: utf-8 -*-


def arg_to_bidirectional_lilypond_symbol(arg):
    r'''Changes `arg` to bidirectional LilyPond symbol.

    ..  container:: example

        ::

            >>> stringtools.arg_to_tridirectional_lilypond_symbol(Up)
            '^'

    ..  container:: example

        ::

            >>> stringtools.arg_to_tridirectional_lilypond_symbol(Down)
            '_'

    ..  container:: example

        ::

            >>> stringtools.arg_to_tridirectional_lilypond_symbol(1)
            '^'

    ..  container:: example

        ::

            >>> stringtools.arg_to_tridirectional_lilypond_symbol(-1)
            '_'

    Returns `arg` when `arg` is `'^'` or `'_'`.

    Returns string or none.
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