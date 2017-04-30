# -*- coding: utf-8 -*-


def to_tridirectional_ordinal_constant(argument):
    r'''Changes `argument` to tridirectional ordinal constant.

    ..  container:: example

            >>> stringtools.to_tridirectional_ordinal_constant('^')
            Up

    ..  container:: example

        ::

            >>> stringtools.to_tridirectional_ordinal_constant('_')
            Down

    ..  container:: example

        ::

            >>> stringtools.to_tridirectional_ordinal_constant(1)
            Up

    ..  container:: example

        ::

            >>> stringtools.to_tridirectional_ordinal_constant(-1)
            Down

    Returns `argument` when `argument` is `Up`', `Center` or `Down`.

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
    if argument is None:
        return None
    elif argument in lookup:
        return lookup[argument]
    message = 'unrecognized expression: {!r}.'
    message = message.format(argument)
    raise ValueError(message)
