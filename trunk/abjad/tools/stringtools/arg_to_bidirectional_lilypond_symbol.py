def arg_to_bidirectional_lilypond_symbol(arg):
    '''Convert `arg` to bidirectional LilyPond symbol:

    ::  

        abjad> from abjad.tools import stringtools

    ::

        abjad> stringtools.arg_to_tridirectional_lilypond_symbol('up')
        '^'

    ::

        abjad> stringtools.arg_to_tridirectional_lilypond_symbol('down')
        '_'

    ::

        abjad> stringtools.arg_to_tridirectional_lilypond_symbol(1)
        '^'

    ::

        abjad> stringtools.arg_to_tridirectional_lilypond_symbol(-1)
        '_'

    If `arg` is '^' or '_', `arg` will be returned.

    Return str or None.
    '''

    lookup = {
        1: '^',
        -1: '_',
        'up': '^',
        'down': '_',
        '^': '^',
        '_': '_',
    }

    if arg in lookup:
        return lookup[arg]
    raise ValueError
