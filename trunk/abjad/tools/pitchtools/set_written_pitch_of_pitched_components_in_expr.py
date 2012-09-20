def set_written_pitch_of_pitched_components_in_expr(expr, written_pitch=0):
    r'''.. versionadded:: 2.9

    Set written pitch of pitched components in `expr` to `written_pitch`::

        >>> staff = Staff("c' d' e' f'")

    ::

        >>> f(staff)
        \new Staff {
            c'4
            d'4
            e'4
            f'4
        }

    ::

        >>> pitchtools.set_written_pitch_of_pitched_components_in_expr(staff)

    ::

        >>> f(staff)
        \new Staff {
            c'4
            c'4
            c'4
            c'4
        }

    Use as a way of neutralizing pitch information in an arbitrary piece of score.

    Return none.
    '''
    from abjad.tools import chordtools
    from abjad.tools import iterationtools
    from abjad.tools import notetools

    for leaf in iterationtools.iterate_leaves_in_expr(expr):
        if isinstance(leaf, notetools.Note):
            leaf.written_pitch = written_pitch
        elif isinstance(leaf, chordtools.Chord):
            leaf.written_pitches = [written_pitch]
