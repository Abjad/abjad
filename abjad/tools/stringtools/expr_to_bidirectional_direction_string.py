# -*- coding: utf-8 -*-


def expr_to_bidirectional_direction_string(expr):
    r'''Changes `expr` to bidirectional direction string.

    ..  container:: example:

        ::

            >>> stringtools.expr_to_bidirectional_direction_string('^')
            'up'

    ..  container:: example:

        ::

            >>> stringtools.expr_to_bidirectional_direction_string('_')
            'down'

    ..  container:: example:

        ::

            >>> stringtools.expr_to_bidirectional_direction_string(1)
            'up'

    ..  container:: example:

        ::

            >>> stringtools.expr_to_bidirectional_direction_string(-1)
            'down'

    Returns `expr` when `expr` is `'up'` or `'down'`.

    Returns string or none.
    '''
    lookup = {
        1: 'up',
        -1: 'down',
        Up: 'up',
        Down: 'down',
        '^': 'up',
        '_': 'down',
        'up': 'up',
        'down': 'down'
        }
    if expr in lookup:
        return lookup[expr]
    raise ValueError(expr)
