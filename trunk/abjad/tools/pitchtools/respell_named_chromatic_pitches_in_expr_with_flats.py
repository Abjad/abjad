def respell_named_chromatic_pitches_in_expr_with_flats(expr):
    r'''.. versionadded:: 1.1

    Respell named chromatic pitches in `expr` with flats::

        >>> staff = Staff(notetools.make_repeated_notes(6))
        >>> pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(staff)

    ::

        >>> f(staff)
        \new Staff {
            c'8
            cs'8
            d'8
            ef'8
            e'8
            f'8
        }

    ::

        >>> pitchtools.respell_named_chromatic_pitches_in_expr_with_flats(staff)

    ::

        >>> f(staff)
        \new Staff {
            c'8
            df'8
            d'8
            ef'8
            e'8
            f'8
        }

    Return none.

    .. versionchanged:: 2.0
        renamed ``pitchtools.make_flat()`` to
        ``pitchtools.respell_named_chromatic_pitches_in_expr_with_flats()``.
    '''
    from abjad.tools import chordtools
    from abjad.tools import iterationtools
    from abjad.tools import pitchtools


    if isinstance(expr, pitchtools.NamedChromaticPitch):
        return _new_pitch_with_flats(expr)
    else:
        for leaf in iterationtools.iterate_leaves_in_expr(expr):
            if isinstance(leaf, chordtools.Chord):
                for note_head in leaf.note_heads:
                    note_head.written_pitch = _new_pitch_with_flats(note_head.written_pitch)
            elif hasattr(leaf, 'written_pitch'):
                leaf.written_pitch = _new_pitch_with_flats(leaf.written_pitch)


# TODO: make public
def _new_pitch_with_flats(pitch):
    from abjad.tools import pitchtools

    octave = pitchtools.chromatic_pitch_number_to_octave_number(abs(pitch.numbered_chromatic_pitch))
    name = pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_flats(
        pitch.numbered_chromatic_pitch_class)
    pitch = type(pitch)(name, octave)

    return pitch
