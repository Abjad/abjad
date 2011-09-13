from abjad.tools.pitchtools.NumberedChromaticPitchClass import NumberedChromaticPitchClass
from abjad.tools.pitchtools.list_named_chromatic_pitches_in_expr import list_named_chromatic_pitches_in_expr


def list_numbered_chromatic_pitch_classes_in_expr(expr):
    '''.. versionadded:: 2.0

    List numbered chromatic pitch-classes in `expr`::

        abjad> chord = Chord([13, 14, 15], (1, 4))
        abjad> pitchtools.list_numbered_chromatic_pitch_classes_in_expr(chord)
        (NumberedChromaticPitchClass(1), NumberedChromaticPitchClass(2), NumberedChromaticPitchClass(3))

    Works with notes, chords, defective chords.

    Return tuple or zero or more numbered chromatic pitch-classes.

    .. versionchanged:: 2.0
        renamed ``pitchtools.list_numeric_chromatic_pitch_classes_in_expr()`` to
        ``pitchtools.list_numbered_chromatic_pitch_classes_in_expr()``.
    '''

    pitches = list_named_chromatic_pitches_in_expr(expr)
    pitch_classes = [NumberedChromaticPitchClass(pitch) for pitch in pitches]
    pitch_classes = tuple(pitch_classes)
    return pitch_classes
