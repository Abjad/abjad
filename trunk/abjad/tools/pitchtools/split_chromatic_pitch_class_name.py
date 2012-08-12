def split_chromatic_pitch_class_name(chromatic_pitch_class_name):
    '''.. versionadded:: 1.1

    Change `chromatic_pitch_class_name` to diatonic pitch-class name / alphabetic
    accidental abbreviation pair::

        >>> pitchtools.split_chromatic_pitch_class_name('cs')
        ('c', 's')

    Return pair of strings.

    .. versionchanged:: 2.0
        renamed ``pitchtools.name_to_letter_accidental()`` to
        ``pitchtools.split_chromatic_pitch_class_name()``.
    '''

    if len(chromatic_pitch_class_name) == 1:
        return chromatic_pitch_class_name, ''
    else:
        return chromatic_pitch_class_name[0], chromatic_pitch_class_name[1:]
