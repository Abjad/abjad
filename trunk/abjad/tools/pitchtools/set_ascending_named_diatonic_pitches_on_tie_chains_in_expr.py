def set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(expr, key_signature=None):
    r'''.. versionadded:: 1.1

    Set ascending named diatonic pitches on nontied pitched components in `expr`::

        >>> staff = Staff(notetools.make_notes(0, [(5, 32)] * 4))
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)

    ::

        >>> f(staff)
        \new Staff {
            c'8 ~
            c'32
            d'8 ~
            d'32
            e'8 ~
            e'32
            f'8 ~
            f'32
        }

    Used primarily in generating test file examples.

    .. versionadded:: 2.0
        Optional `key_signature` keyword argument.

    Return none.

    .. versionchanged:: 2.0
        renamed ``pitchtools.diatonicize()`` to
        ``pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr()``.
    '''
    from abjad.tools import chordtools
    from abjad.tools import iterationtools
    from abjad.tools import notetools
    from abjad.tools import pitchtools
    from abjad.tools import tietools
    from abjad.tools import tonalitytools

    if key_signature is None:
        scale = tonalitytools.Scale('C', 'major')
    else:
        scale = tonalitytools.Scale(key_signature)

    dicg = scale.diatonic_interval_class_segment
    length = len(dicg)

    octave_number = 4
    pitch = pitchtools.NamedChromaticPitch(scale[0], octave_number)

    for i, tie_chain in enumerate(tietools.iterate_tie_chains_in_expr(expr)):
        if isinstance(tie_chain[0], notetools.Note):
            for note in tie_chain:
                note.written_pitch = pitch
        elif isinstance(tie_chain[0], chordtools.Chord):
            for chord in tie_chain:
                chord.written_pitches = [pitch]
        else:
            pass
        dic = dicg[i % length]
        ascending_mdi = pitchtools.MelodicDiatonicInterval(dic.quality_string, dic.number)
        pitch += ascending_mdi
