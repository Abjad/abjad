def chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_sharps(chromatic_pitch_class_number):
    '''.. versionadded:: 1.1

    Change `chromatic_pitch_class_number` to chromatic pitch-class name with sharps::

        abjad> for n in range(13):
        ...     pc = n / 2.0
        ...     name = pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_sharps(pc)
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

    .. versionchanged:: 2.0
        renamed ``pitchtools.pc_to_pitch_name_sharps()`` to
        ``pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_sharps()``.
    '''

    try:
        return _pitch_class_number_to_pitch_class_name_sharps[chromatic_pitch_class_number]
    except KeyError:
        return _pitch_class_number_to_pitch_class_name_sharps[abs(chromatic_pitch_class_number)]


_pitch_class_number_to_pitch_class_name_sharps = {
        0:  'c',     0.5: 'cqs',    1: 'cs',    1.5:  'ctqs',
        2:  'd',     2.5: 'dqs',    3: 'ds',    3.5:  'dtqs',
        4:  'e',     4.5: 'eqs',    5: 'f',     5.5:  'fqs',
        6:  'fs',    6.5: 'ftqs',   7: 'g',     7.5:  'gqs',
        8:  'gs',    8.5: 'gtqs',   9: 'a',     9.5:  'aqs',
        10: 'as',   10.5: 'atqs',  11: 'b',    11.5:  'bqs' }
