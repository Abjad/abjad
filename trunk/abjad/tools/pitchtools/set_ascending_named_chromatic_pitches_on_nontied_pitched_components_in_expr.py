def set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(expr):
    r'''.. versionadded:: 1.1

    Set ascending named chromatic pitches on nontied pitched components in `expr`::

        abjad> staff = Voice(notetools.make_notes(0, [(5, 32)] * 4))
        abjad> pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(staff)

    ::

        abjad> f(staff)
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
    from abjad.tools import tietools
    from abjad.tools.chordtools.Chord import Chord
    from abjad.tools.notetools.Note import Note

    for i, x in enumerate(tietools.iterate_tie_chains_forward_in_expr(expr)):
        pitch = i
        if isinstance(x[0], Note):
            for note in x:
                note.written_pitch = pitch
        elif isinstance(x[0], Chord):
            for chord in x:
                chord.written_pitches = [pitch]
        else:
            pass
