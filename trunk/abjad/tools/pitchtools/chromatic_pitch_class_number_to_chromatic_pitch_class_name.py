def chromatic_pitch_class_number_to_chromatic_pitch_class_name(chromatic_pitch_class_number):
    '''.. versionadded:: 1.1

    Change `chromatic_pitch_class_number` to chromatic pitch-class name::

        abjad> for n in range(0, 13):
        ...     pc = n / 2.0
        ...     pitch_name = pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name(pc)
        ...     print '%s   %s' % (pc, pitch_name)
        ...
        0.0   c
        0.5   cqs
        1.0   cs
        1.5   dqf
        2.0   d
        2.5   dqs
        3.0   ef
        3.5   eqf
        4.0   e
        4.5   eqs
        5.0   f
        5.5   fqs
        6.0   fs

    Return string.

    .. versionchanged:: 2.0
        renamed ``pitchtools.pc_to_pitch_name()`` to
        ``pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name()``.
    '''

    return _pitch_class_number_to_pitch_class_name[chromatic_pitch_class_number]


_pitch_class_number_to_pitch_class_name = {
    0:  'c',      0.5: 'cqs',     1: 'cs',     1.5:  'dqf',
    2:  'd',      2.5: 'dqs',     3: 'ef',     3.5:  'eqf',
    4:  'e',      4.5: 'eqs',     5: 'f',      5.5:  'fqs',
    6:  'fs',     6.5: 'gqf',     7: 'g',      7.5:  'gqs',
    8:  'af',     8.5: 'aqf',     9: 'a',      9.5:  'aqs',
    10: 'bf',    10.5: 'bqf',    11: 'b',     11.5:  'bqs' }
