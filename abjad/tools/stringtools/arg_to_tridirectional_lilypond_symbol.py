# -*- encoding: utf-8 -*-


def arg_to_tridirectional_lilypond_symbol(arg):
    r'''Changes `arg` to tridirectional LilyPond symbol.

    ..  container:: example

        ::

            >>> stringtools.arg_to_tridirectional_lilypond_symbol(Up)
            '^'

    ..  container:: example

        ::

            >>> stringtools.arg_to_tridirectional_lilypond_symbol('neutral')
            '-'

    ..  container:: example

        ::

            >>> stringtools.arg_to_tridirectional_lilypond_symbol('default')
            '-'

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

            >>> stringtools.arg_to_tridirectional_lilypond_symbol(0)
            '-'

    ..  container:: example

        ::

            >>> stringtools.arg_to_tridirectional_lilypond_symbol(-1)
            '_'

    Returns none when `arg` is none.

    Returns `arg` when `arg` is `'^'`, `'-'` or `'_'`.

    Returns string or none.
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