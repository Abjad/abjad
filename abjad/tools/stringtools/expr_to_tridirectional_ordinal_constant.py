# -*- coding: utf-8 -*-


def expr_to_tridirectional_ordinal_constant(expr):
    r'''Changes `expr` to tridirectional ordinal constant.

    ..  container:: example

            >>> stringtools.expr_to_tridirectional_ordinal_constant('^')
            Up

    ..  container:: example

        ::

            >>> stringtools.expr_to_tridirectional_ordinal_constant('_')
            Down

    ..  container:: example

        ::

            >>> stringtools.expr_to_tridirectional_ordinal_constant(1)
            Up

    ..  container:: example

        ::

            >>> stringtools.expr_to_tridirectional_ordinal_constant(-1)
            Down

    Returns `expr` when `expr` is `Up`', `Center` or `Down`.

    Returns ordinal constant or none.
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
    if expr is None:
        return None
    elif expr in lookup:
        return lookup[expr]
    message = 'unrecognized expression: {!r}.'
    message = message.format(expr)
    raise ValueError(message)
