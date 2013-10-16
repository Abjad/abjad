# -*- encoding: utf-8 -*-
from abjad.tools import mathtools


def spell_numbered_interval_number(diatonic_interval_number, numbered_interval_number):
    '''Spell `numbered_interval_number` according to `diatonic_interval_number`:

    ::

        >>> pitchtools.spell_numbered_interval_number(2, 1)
        NamedInterval('+m2')

    Return melodic diatonic interval.
    '''
    from abjad.tools import pitchtools

    if not isinstance(numbered_interval_number, int):
        raise IntervalError('can not determine diatonic interval from float.')

    direction_number = mathtools.sign(numbered_interval_number)

    if diatonic_interval_number == 1:
        if numbered_interval_number % 12 == 11:
            quality_string = 'augmented'
        elif numbered_interval_number % 12 == 0:
            quality_string = 'perfect'
        elif numbered_interval_number % 12 == 1:
            quality_string = 'augmented'
        if not direction_number == 0:
            diatonic_interval_number *= direction_number
        diatonic_interval = pitchtools.NamedInterval(quality_string, diatonic_interval_number)
        return diatonic_interval

    diatonic_interval_class_number = diatonic_interval_number % 7
    numbered_interval_class_number = abs(numbered_interval_number) % 12

    if diatonic_interval_class_number == 0:
        if numbered_interval_class_number == 9:
            quality_string = 'diminished'
        elif numbered_interval_class_number == 10:
            quality_string = 'minor'
        elif numbered_interval_class_number == 11:
            quality_string = 'major'
        elif numbered_interval_class_number == 0:
            quality_string = 'augmented'
    elif diatonic_interval_class_number == 1:
        if numbered_interval_class_number == 11:
            quality_string = 'diminished'
        elif numbered_interval_class_number == 0:
            quality_string = 'perfect'
        elif numbered_interval_class_number == 1:
            quality_string = 'augmented'
    elif diatonic_interval_class_number == 2:
        if numbered_interval_class_number == 0:
            quality_string = 'diminished'
        elif numbered_interval_class_number == 1:
            quality_string = 'minor'
        elif numbered_interval_class_number == 2:
            quality_string = 'major'
        elif numbered_interval_class_number == 3:
            quality_string = 'augmented'
    elif diatonic_interval_class_number == 3:
        if numbered_interval_class_number == 2:
            quality_string = 'diminished'
        elif numbered_interval_class_number == 3:
            quality_string = 'minor'
        elif numbered_interval_class_number == 4:
            quality_string = 'major'
        elif numbered_interval_class_number == 5:
            quality_string = 'augmented'
    elif diatonic_interval_class_number == 4:
        if numbered_interval_class_number == 4:
            quality_string = 'diminished'
        elif numbered_interval_class_number == 5:
            quality_string = 'perfect'
        elif numbered_interval_class_number == 6:
            quality_string = 'augmented'
    elif diatonic_interval_class_number == 5:
        if numbered_interval_class_number == 6:
            quality_string = 'diminished'
        elif numbered_interval_class_number == 7:
            quality_string = 'perfect'
        elif numbered_interval_class_number == 8:
            quality_string = 'augmented'
    elif diatonic_interval_class_number == 6:
        if numbered_interval_class_number == 7:
            quality_string = 'diminished'
        elif numbered_interval_class_number == 8:
            quality_string = 'minor'
        elif numbered_interval_class_number == 9:
            quality_string = 'major'
        elif numbered_interval_class_number == 10:
            quality_string = 'augmented'
    elif diatonic_interval_class_number == 7:
        if numbered_interval_class_number == 9:
            quality_string = 'diminished'
        elif numbered_interval_class_number == 10:
            quality_string = 'minor'
        elif numbered_interval_class_number == 11:
            quality_string = 'major'
        elif numbered_interval_class_number == 0:
            quality_string = 'augmented'
    elif diatonic_interval_class_number == 8:
        if numbered_interval_class_number == 11:
            quality_string = 'diminished'
        elif numbered_interval_class_number == 0:
            quality_string = 'perfect'
        elif numbered_interval_class_number == 1:
            quality_string = 'augmented'

    if not direction_number == 0:
        diatonic_interval_number *= direction_number

    diatonic_interval = pitchtools.NamedInterval(quality_string, diatonic_interval_number)

    return diatonic_interval
