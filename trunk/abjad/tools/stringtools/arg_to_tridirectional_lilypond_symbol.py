def arg_to_tridirectional_lilypond_symbol(arg):
    '''Convert `arg` to tridirectional LilyPond symbol:

    ::  

        abjad> from abjad.tools import stringtools

    ::

        abjad> stringtools.arg_to_tridirectional_lilypond_symbol('up')
        '^'

    ::

        abjad> stringtools.arg_to_tridirectional_lilypond_symbol('neutral')
        '-'

    ::

        abjad> stringtools.arg_to_tridirectional_lilypond_symbol('default')
        '-'

    ::

        abjad> stringtools.arg_to_tridirectional_lilypond_symbol('down')
        '_'

    ::

        abjad> stringtools.arg_to_tridirectional_lilypond_symbol(1)
        '^'

    ::

        abjad> stringtools.arg_to_tridirectional_lilypond_symbol(0)
        '-'

    ::

        abjad> stringtools.arg_to_tridirectional_lilypond_symbol(-1)
        '_'

    If `arg` is None, None will be returned.

    If `arg` is '^', '-', or '_', `arg` will be returned.

    Return string or None.
    '''

    lookup = {
        1: '^',
        0: '-',
        -1: '_',
        'up': '^',
        'neutral': '-',
        'default': '-',
        'down': '_',
        '^': '^',
        '-': '-',
        '_': '_',
    }

    if arg is None:
        return None 
    elif arg in lookup:
        return lookup[arg]
    raise ValueError
