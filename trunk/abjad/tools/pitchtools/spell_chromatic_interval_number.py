from abjad.tools import mathtools


def spell_chromatic_interval_number(diatonic_interval_number, chromatic_interval_number):
    '''.. versionadded:: 2.0

    Spell `chromatic_interval_number` according to `diatonic_interval_number`::

        >>> pitchtools.spell_chromatic_interval_number(2, 1)
        MelodicDiatonicInterval('+m2')

    Return melodic diatonic interval.
    '''
    from abjad.tools import pitchtools

    if not isinstance(chromatic_interval_number, int):
        raise IntervalError('can not determine diatonic interval from float.')

    direction_number = mathtools.sign(chromatic_interval_number)

    if diatonic_interval_number == 1:
        if chromatic_interval_number % 12 == 11:
            quality_string = 'augmented'
        elif chromatic_interval_number % 12 == 0:
            quality_string = 'perfect'
        elif chromatic_interval_number % 12 == 1:
            quality_string = 'augmented'
        if not direction_number == 0:
            diatonic_interval_number *= direction_number
        diatonic_interval = pitchtools.MelodicDiatonicInterval(quality_string, diatonic_interval_number)
        return diatonic_interval

    diatonic_interval_class_number = diatonic_interval_number % 7
    chromatic_interval_class_number = abs(chromatic_interval_number) % 12

    if diatonic_interval_class_number == 0:
        if chromatic_interval_class_number == 9:
            quality_string = 'diminished'
        elif chromatic_interval_class_number == 10:
            quality_string = 'minor'
        elif chromatic_interval_class_number == 11:
            quality_string = 'major'
        elif chromatic_interval_class_number == 0:
            quality_string = 'augmented'
    elif diatonic_interval_class_number == 1:
        if chromatic_interval_class_number == 11:
            quality_string = 'diminished'
        elif chromatic_interval_class_number == 0:
            quality_string = 'perfect'
        elif chromatic_interval_class_number == 1:
            quality_string = 'augmented'
    elif diatonic_interval_class_number == 2:
        if chromatic_interval_class_number == 0:
            quality_string = 'diminished'
        elif chromatic_interval_class_number == 1:
            quality_string = 'minor'
        elif chromatic_interval_class_number == 2:
            quality_string = 'major'
        elif chromatic_interval_class_number == 3:
            quality_string = 'augmented'
    elif diatonic_interval_class_number == 3:
        if chromatic_interval_class_number == 2:
            quality_string = 'diminished'
        elif chromatic_interval_class_number == 3:
            quality_string = 'minor'
        elif chromatic_interval_class_number == 4:
            quality_string = 'major'
        elif chromatic_interval_class_number == 5:
            quality_string = 'augmented'
    elif diatonic_interval_class_number == 4:
        if chromatic_interval_class_number == 4:
            quality_string = 'diminished'
        elif chromatic_interval_class_number == 5:
            quality_string = 'perfect'
        elif chromatic_interval_class_number == 6:
            quality_string = 'augmented'
    elif diatonic_interval_class_number == 5:
        if chromatic_interval_class_number == 6:
            quality_string = 'diminished'
        elif chromatic_interval_class_number == 7:
            quality_string = 'perfect'
        elif chromatic_interval_class_number == 8:
            quality_string = 'augmented'
    elif diatonic_interval_class_number == 6:
        if chromatic_interval_class_number == 7:
            quality_string = 'diminished'
        elif chromatic_interval_class_number == 8:
            quality_string = 'minor'
        elif chromatic_interval_class_number == 9:
            quality_string = 'major'
        elif chromatic_interval_class_number == 10:
            quality_string = 'augmented'
    elif diatonic_interval_class_number == 7:
        if chromatic_interval_class_number == 9:
            quality_string = 'diminished'
        elif chromatic_interval_class_number == 10:
            quality_string = 'minor'
        elif chromatic_interval_class_number == 11:
            quality_string = 'major'
        elif chromatic_interval_class_number == 0:
            quality_string = 'augmented'
    elif diatonic_interval_class_number == 8:
        if chromatic_interval_class_number == 11:
            quality_string = 'diminished'
        elif chromatic_interval_class_number == 0:
            quality_string = 'perfect'
        elif chromatic_interval_class_number == 1:
            quality_string = 'augmented'

    if not direction_number == 0:
        diatonic_interval_number *= direction_number

    diatonic_interval = pitchtools.MelodicDiatonicInterval(quality_string, diatonic_interval_number)

    return diatonic_interval
