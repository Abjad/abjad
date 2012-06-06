def set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(expr):
    r'''.. versionadded:: 1.1

    Set ascending named chromatic pitches on nontied pitched components in `expr`::

        >>> staff = Voice(notetools.make_notes(0, [(5, 32)] * 4))
        >>> pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(staff)

    ::

        >>> f(staff)
        \new Voice {
            c'8 ~
            c'32
            cs'8 ~
            cs'32
            d'8 ~
            d'32
            ef'8 ~
            ef'32
        }

    Used primarily in generating test file examples.

    Return none.

    .. versionchanged:: 2.0
        renamed ``pitchtools.chromaticize()`` to
        ``pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr()``.
    '''
    from abjad.tools import chordtools
    from abjad.tools import notetools
    from abjad.tools import tietools

    for i, tie_chain in enumerate(tietools.iterate_tie_chains_forward_in_expr(expr)):
        pitch = i
        if isinstance(tie_chain[0], notetools.Note):
            for note in tie_chain:
                note.written_pitch = pitch
        elif isinstance(tie_chain[0], chordtools.Chord):
            for chord in tie_chain:
                chord.written_pitches = [pitch]
