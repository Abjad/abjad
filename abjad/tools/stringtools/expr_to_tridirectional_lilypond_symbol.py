# -*- coding: utf-8 -*-


def expr_to_tridirectional_lilypond_symbol(expr):
    r'''Changes `expr` to tridirectional LilyPond symbol.

    ..  container:: example

        ::

            >>> stringtools.expr_to_tridirectional_lilypond_symbol(Up)
            '^'

    ..  container:: example

        ::

            >>> stringtools.expr_to_tridirectional_lilypond_symbol('neutral')
            '-'

    ..  container:: example

        ::

            >>> stringtools.expr_to_tridirectional_lilypond_symbol('default')
            '-'

    ..  container:: example

        ::

            >>> stringtools.expr_to_tridirectional_lilypond_symbol(Down)
            '_'

    ..  container:: example

        ::

            >>> stringtools.expr_to_tridirectional_lilypond_symbol(1)
            '^'

    ..  container:: example

        ::

            >>> stringtools.expr_to_tridirectional_lilypond_symbol(0)
            '-'

    ..  container:: example

        ::

            >>> stringtools.expr_to_tridirectional_lilypond_symbol(-1)
            '_'

    Returns none when `expr` is none.

    Returns `expr` when `expr` is `'^'`, `'-'` or `'_'`.

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
    if expr is None:
        return None
    elif expr in lookup:
        return lookup[expr]
    raise ValueError(expr)
