def arg_to_bidirectional_direction_string(arg):
    '''Convert `arg` to bidirectional direction string:

    ::

        abjad> from abjad.tools import stringtools

    ::

        abjad> stringtools.arg_to_bidirectional_direction_string('^')
        'up'

    ::

        abjad> stringtools.arg_to_bidirectional_direction_string('_')
        'down'

    ::

        abjad> stringtools.arg_to_bidirectional_direction_string(1)
        'up'

    ::

        abjad> stringtools.arg_to_bidirectional_direction_string(-1)
        'down'

    If `arg` is 'up' or 'down', `arg` will be returned.

    Return str or None.
    '''

    lookup = { 
        1: 'up',
        -1: 'down',
        'up': 'up',
        'down': 'down',
        '^': 'up',
        '_': 'down',
    }

    if arg in lookup:
        return lookup[arg]
    raise ValueError
