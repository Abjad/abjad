# -*- coding: utf-8 -*-


def expr_to_bidirectional_lilypond_symbol(expr):
    r'''Changes `expr` to bidirectional LilyPond symbol.

    ..  container:: example

        ::

            >>> stringtools.expr_to_tridirectional_lilypond_symbol(Up)
            '^'

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

            >>> stringtools.expr_to_tridirectional_lilypond_symbol(-1)
            '_'

    Returns `expr` when `expr` is `'^'` or `'_'`.

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
    if expr in lookup:
        return lookup[expr]
    raise ValueError(expr)
