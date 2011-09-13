from abjad.tools.pitchtools.NamedChromaticPitchSet import NamedChromaticPitchSet
from abjad.tools.pitchtools.list_named_chromatic_pitches_in_expr import list_named_chromatic_pitches_in_expr


def expr_has_duplicate_named_chromatic_pitch(expr):
    '''.. versionadded:: 2.0

    True when `expr` has duplicate named chromatic pitch.
    Otherwise false::

        abjad> chord = Chord([13, 13, 14], (1, 4))
        abjad> pitchtools.expr_has_duplicate_named_chromatic_pitch(chord)
        True

    Return boolean.
    '''

    pitches = list_named_chromatic_pitches_in_expr(expr)
    pitch_set = NamedChromaticPitchSet(pitches)
    return not len(pitches) == len(pitch_set)
