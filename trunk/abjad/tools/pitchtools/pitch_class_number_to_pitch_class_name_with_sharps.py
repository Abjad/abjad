# -*- encoding: utf-8 -*-


def pitch_class_number_to_pitch_class_name_with_sharps(pitch_class_number):
    '''Change `pitch_class_number` to chromatic pitch-class name with sharps:

    ::

        >>> tmp = pitchtools.pitch_class_number_to_pitch_class_name_with_sharps
        >>> for n in range(13):
        ...     pc = n / 2.0
        ...     name = tmp(pc)
        ...     print '%s   %s' % (pc, name)
        ...
        0.0   c
        0.5   cqs
        1.0   cs
        1.5   ctqs
        2.0   d
        2.5   dqs
        3.0   ds
        3.5   dtqs
        4.0   e
        4.5   eqs
        5.0   f
        5.5   fqs
        6.0   fs

    Return string.
    '''
    from abjad.tools import pitchtools
    try:
        return pitchtools.PitchClass._pitch_class_number_to_pitch_class_name_with_sharps[
            pitch_class_number]
    except KeyError:
        return pitchtools.PitchClass._pitch_class_number_to_pitch_class_name_with_sharps[
            abs(pitch_class_number)]
