# -*- encoding: utf-8 -*-


def arg_to_tridirectional_ordinal_constant(arg):
    r'''Changes `arg` to tridirectional ordinal constant.

    ..  container:: example

            >>> stringtools.arg_to_tridirectional_ordinal_constant('^')
            Up

    ..  container:: example

        ::

            >>> stringtools.arg_to_tridirectional_ordinal_constant('_')
            Down

    ..  container:: example

        ::

            >>> stringtools.arg_to_tridirectional_ordinal_constant(1)
            Up

    ..  container:: example

        ::

            >>> stringtools.arg_to_tridirectional_ordinal_constant(-1)
            Down

    Returns `arg` when `arg` is `Up`', `Center` or `Down`.

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
    if arg is None:
        return None
    elif arg in lookup:
        return lookup[arg]
    raise ValueError(arg)