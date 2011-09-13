from abjad.tools.pitchtools.is_named_chromatic_pitch_token import is_named_chromatic_pitch_token


def all_are_chromatic_pitch_class_name_octave_number_pairs(expr):
    '''.. versionadded:: 1.1

    True when all elements of `expr` are pitch tokens. Otherwise false::

        abjad> pitchtools.all_are_chromatic_pitch_class_name_octave_number_pairs([('c', 4), ('d', 4), pitchtools.NamedChromaticPitch('e', 4)])
        True

    Return boolean.

    .. versionchanged:: 2.0
        renamed ``pitchtools.is_pitch_token_collection()`` to
        ``pitchtools.all_are_chromatic_pitch_class_name_octave_number_pairs()``.
    '''

    if isinstance(expr, (list, tuple, set)):
        if all([is_named_chromatic_pitch_token(x) for x in expr]):
            return True
    return False
