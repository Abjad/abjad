# -*- coding: utf-8 -*-


def expr_to_tridirectional_direction_string(expr):
    r'''Changes `expr` to tridirectional direction string.

    ..  container:: example

        ::

            >>> stringtools.expr_to_tridirectional_direction_string('^')
            'up'

    ..  container:: example

        ::

            >>> stringtools.expr_to_tridirectional_direction_string('-')
            'center'

    ..  container:: example

        ::

            >>> stringtools.expr_to_tridirectional_direction_string('_')
            'down'

    ..  container:: example

        ::

            >>> stringtools.expr_to_tridirectional_direction_string(1)
            'up'

    ..  container:: example

        ::

            >>> stringtools.expr_to_tridirectional_direction_string(0)
            'center'

    ..  container:: example

        ::

            >>> stringtools.expr_to_tridirectional_direction_string(-1)
            'down'

    ..  container:: example

        ::

            >>> stringtools.expr_to_tridirectional_direction_string('default')
            'center'

    Returns none when `expr` is none.

    Returns string or none.
    '''
    lookup = {
        Up: 'up',
        '^': 'up',
        'up': 'up',
        1: 'up',
        Down: 'down',
        '_': 'down',
        'down': 'down',
        -1: 'down',
        Center: 'center',
        '-': 'center',
        0: 'center',
        'center': 'center',
        'default': 'center',
        'neutral': 'center',
        }
    if expr is None:
        return None
    elif expr in lookup:
        return lookup[expr]
    raise ValueError(expr)
