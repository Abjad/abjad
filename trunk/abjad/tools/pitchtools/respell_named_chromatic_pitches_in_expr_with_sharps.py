from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch
from abjad.tools.pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_sharps import chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_sharps
from abjad.tools.pitchtools.chromatic_pitch_number_to_octave_number import chromatic_pitch_number_to_octave_number


def respell_named_chromatic_pitches_in_expr_with_sharps(expr):
    r'''.. versionadded:: 1.1

    Respell named chromatic pitches in `expr` with sharps::

        abjad> staff = Staff(notetools.make_repeated_notes(6))
        abjad> pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(staff)

    ::

        abjad> f(staff)
        \new Staff {
            c'8
            cs'8
            d'8
            ef'8
            e'8
            f'8
        }

    ::

        abjad> pitchtools.respell_named_chromatic_pitches_in_expr_with_sharps(staff)

    ::

        abjad> f(staff)
        \new Staff {
            c'8
            cs'8
            d'8
            ds'8
            e'8
            f'8
        }

    Return none.

    .. versionchanged:: 2.0
        renamed ``pitchtools.make_sharp()`` to
        ``pitchtools.respell_named_chromatic_pitches_in_expr_with_sharps()``.
    '''
    from abjad.tools.chordtools.Chord import Chord
    from abjad.tools import leaftools

    if isinstance(expr, NamedChromaticPitch):
        return _new_pitch_with_sharps(expr)
    else:
        for leaf in leaftools.iterate_leaves_forward_in_expr(expr):
            if isinstance(leaf, Chord):
                for note_head in leaf.note_heads:
                    note_head.written_pitch = _new_pitch_with_sharps(note_head.written_pitch)
            elif hasattr(leaf, 'written_pitch'):
                leaf.written_pitch = _new_pitch_with_sharps(leaf.written_pitch)


def _new_pitch_with_sharps(pitch):
    octave = chromatic_pitch_number_to_octave_number(abs(pitch.numbered_chromatic_pitch))
    name = chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_sharps(
        pitch.numbered_chromatic_pitch_class)
    pitch = type(pitch)(name, octave)
    return pitch
