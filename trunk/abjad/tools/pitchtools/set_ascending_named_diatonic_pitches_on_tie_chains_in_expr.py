# -*- encoding: utf-8 -*-


def set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(expr, key_signature=None):
    r'''Set ascending named diatonic pitches on nontied pitched components in `expr`:

    ::

        >>> staff = Staff(notetools.make_notes(0, [(5, 32)] * 4))
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)

    ..  doctest::

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

    Optional `key_signature` keyword argument.

    Return none.
    '''
    from abjad.tools import chordtools
    from abjad.tools import iterationtools
    from abjad.tools import notetools
    from abjad.tools import pitchtools
    from abjad.tools import tonalanalysistools

    if key_signature is None:
        scale = tonalanalysistools.Scale('C', 'major')
    else:
        scale = tonalanalysistools.Scale(key_signature)

    dicg = scale.diatonic_interval_class_segment
    length = len(dicg)

    octave_number = 4
    pitch = pitchtools.NamedPitch(scale[0], octave_number)

    for i, tie_chain in enumerate(iterationtools.iterate_tie_chains_in_expr(expr)):
        if isinstance(tie_chain[0], notetools.Note):
            for note in tie_chain:
                note.written_pitch = pitch
        elif isinstance(tie_chain[0], chordtools.Chord):
            for chord in tie_chain:
                chord.written_pitches = [pitch]
        else:
            pass
        dic = dicg[i % length]
        ascending_mdi = pitchtools.NamedInterval(dic.quality_string, dic.number)
        pitch += ascending_mdi
