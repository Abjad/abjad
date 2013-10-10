# -*- encoding: utf-8 -*-


def pitch_class_number_to_pitch_class_name_with_flats(pitch_class_number):
    '''Change chromatic pitch-class number to chromatic pitch-class name with flats:

    ::

        >>> tmp = pitchtools.pitch_class_number_to_pitch_class_name_with_flats

    ::

        >>> for n in range(13):
        ...     pc = n / 2.0
        ...     name = tmp(pc)
        ...     print '%s   %s' % (pc, name)
        ...
        0.0   c
        0.5   dtqf
        1.0   df
        1.5   dqf
        2.0   d
        2.5   etqf
        3.0   ef
        3.5   eqf
        4.0   e
        4.5   fqf
        5.0   f
        5.5   gtqf
        6.0   gf

    Return string.
    '''
    from abjad.tools import pitchtools
    try:
        return pitchtools.PitchClass._pitch_class_number_to_pitch_class_name_with_flats[
            pitch_class_number]
    except KeyError:
        return pitchtools.PitchClass._pitch_class_number_to_pitch_class_name_with_flats[
            abs(pitch_class_number)]
