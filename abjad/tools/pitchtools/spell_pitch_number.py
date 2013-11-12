# -*- encoding: utf-8 -*-
import math


def spell_pitch_number(pitch_number, diatonic_pitch_class_name):
    '''Spell `pitch_number` according to `diatonic_pitch_class_name`:

    ::

        >>> pitchtools.spell_pitch_number(14, 'c')
        (Accidental('ss'), 5)

    Returns accidental / octave-number pair.
    '''
    from abjad.tools import pitchtools

    # check input
    if not isinstance(pitch_number, (int, long, float)):
        raise TypeError

    if not isinstance(diatonic_pitch_class_name, str):
        raise TypeError

    if not diatonic_pitch_class_name in ['c', 'd', 'e', 'f', 'g', 'a', 'b']:
        raise ValueError

    # find accidental semitones
    pc = \
        pitchtools.PitchClass._diatonic_pitch_class_name_to_pitch_class_number[
            diatonic_pitch_class_name]
    nearest_neighbor = pitchtools.transpose_pitch_class_number_to_pitch_number_neighbor(
        pitch_number, pc)
    semitones = pitch_number - nearest_neighbor

    # find accidental alphabetic string
    abbreviation = \
        pitchtools.Accidental._semitones_to_abbreviation[
            semitones]
    accidental = pitchtools.Accidental(abbreviation)

    # find octave
    octave_number = int(math.floor((pitch_number - semitones) / 12)) + 4

    # return accidental and octave
    return accidental, octave_number
