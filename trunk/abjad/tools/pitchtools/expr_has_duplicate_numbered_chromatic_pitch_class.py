# -*- encoding: utf-8 -*-


def expr_has_duplicate_numbered_chromatic_pitch_class(expr):
    '''True when `expr` has duplicate numbered chromatic pitch-class.
    Otherwise false:

    ::

        >>> chord = Chord([1, 13, 14], (1, 4))
        >>> pitchtools.expr_has_duplicate_numbered_chromatic_pitch_class(chord)
        True

    Return boolean.
    '''
    from abjad.tools import notetools
    from abjad.tools import pitchtools

    pitch_classes = pitchtools.list_numbered_chromatic_pitch_classes_in_expr(expr)
    if not pitchtools.is_pitch_carrier(expr):
        expr = []
    elif isinstance(expr, notetools.Note):
        expr = [expr]
    pitch_class_set = pitchtools.PitchClassSet(
        expr,
        item_class=pitchtools.NumberedPitchClass,
        )

    return not len(pitch_classes) == len(pitch_class_set)
