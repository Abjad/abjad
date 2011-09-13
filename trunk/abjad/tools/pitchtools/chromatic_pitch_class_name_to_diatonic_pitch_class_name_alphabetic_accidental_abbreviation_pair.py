def chromatic_pitch_class_name_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_pair(  chromatic_pitch_class_name):
    '''.. versionadded:: 1.1

    Change `chromatic_pitch_class_name` to diatonic pitch-class name / alphabetic
    accidental abbreviation pair::

        abjad> pitchtools.chromatic_pitch_class_name_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_pair('cs')
        ('c', 's')

    Return pair of strings.

    .. versionchanged:: 2.0
        renamed ``pitchtools.name_to_letter_accidental()`` to
        ``pitchtools.chromatic_pitch_class_name_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_pair()``.
    '''

    if len(chromatic_pitch_class_name) == 1:
        return chromatic_pitch_class_name, ''
    else:
        return chromatic_pitch_class_name[0], chromatic_pitch_class_name[1:]
