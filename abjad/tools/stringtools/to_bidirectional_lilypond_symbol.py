# -*- coding: utf-8 -*-


def to_bidirectional_lilypond_symbol(argument):
    r'''Changes `argument` to bidirectional LilyPond symbol.

    ..  container:: example

        ::

            >>> stringtools.to_tridirectional_lilypond_symbol(Up)
            '^'

    ..  container:: example

        ::

            >>> stringtools.to_tridirectional_lilypond_symbol(Down)
            '_'

    ..  container:: example

        ::

            >>> stringtools.to_tridirectional_lilypond_symbol(1)
            '^'

    ..  container:: example

        ::

            >>> stringtools.to_tridirectional_lilypond_symbol(-1)
            '_'

    Returns `argument` when `argument` is `'^'` or `'_'`.

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
    if argument in lookup:
        return lookup[argument]
    raise ValueError(argument)
