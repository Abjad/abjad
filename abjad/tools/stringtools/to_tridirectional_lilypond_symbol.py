# -*- coding: utf-8 -*-


def to_tridirectional_lilypond_symbol(argument):
    r'''Changes `argument` to tridirectional LilyPond symbol.

    ..  container:: example

        ::

            >>> stringtools.to_tridirectional_lilypond_symbol(Up)
            '^'

    ..  container:: example

        ::

            >>> stringtools.to_tridirectional_lilypond_symbol('neutral')
            '-'

    ..  container:: example

        ::

            >>> stringtools.to_tridirectional_lilypond_symbol('default')
            '-'

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

            >>> stringtools.to_tridirectional_lilypond_symbol(0)
            '-'

    ..  container:: example

        ::

            >>> stringtools.to_tridirectional_lilypond_symbol(-1)
            '_'

    Returns none when `argument` is none.

    Returns `argument` when `argument` is `'^'`, `'-'` or `'_'`.

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
    if argument is None:
        return None
    elif argument in lookup:
        return lookup[argument]
    raise ValueError(argument)
