def is_chromatic_pitch_class_name_octave_number_pair(expr):
    '''.. versionadded:: 1.1

    True when `arg` has the form of a chromatic pitch-class / octave number pair.
    Otherwise false::

        >>> pitchtools.is_chromatic_pitch_class_name_octave_number_pair(('cs', 5))
        True

    Return boolean.

    .. versionchanged:: 2.0
        renamed ``pitchtools.is_pair()`` to
        ``pitchtools.is_chromatic_pitch_class_name_octave_number_pair()``.
    '''
    from abjad.tools import pitchtools

    if isinstance(expr, tuple):
        if len(expr) == 2:
            if pitchtools.is_chromatic_pitch_class_name(expr[0]):
                if isinstance(expr[1], (int, long)):
                    return True
    return False
