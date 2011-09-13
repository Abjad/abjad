from abjad.tools.pitchtools.NumberedChromaticPitchClassSet import NumberedChromaticPitchClassSet
from abjad.tools.pitchtools.list_numbered_chromatic_pitch_classes_in_expr import list_numbered_chromatic_pitch_classes_in_expr


def expr_has_duplicate_numbered_chromatic_pitch_class(expr):
    '''.. versionadded:: 2.0

    True when `expr` has duplicate numbered chromatic pitch-class.
    Otherwise false::

        abjad> chord = Chord([1, 13, 14], (1, 4))
        abjad> pitchtools.expr_has_duplicate_numbered_chromatic_pitch_class(chord)
        True

    Return boolean.

    .. versionchanged:: 2.0
        renamed ``pitchtools.expr_has_duplicate_numeric_chromatic_pitch_class()`` to
        ``pitchtools.expr_has_duplicate_numbered_chromatic_pitch_class()``.
    '''

    pitch_classes = list_numbered_chromatic_pitch_classes_in_expr(expr)
    pitch_class_set = NumberedChromaticPitchClassSet(expr)
    return not len(pitch_classes) == len(pitch_class_set)
