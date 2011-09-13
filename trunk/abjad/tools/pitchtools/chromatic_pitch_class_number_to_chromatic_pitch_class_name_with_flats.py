def chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_flats(
    chromatic_pitch_class_number):
    '''.. versionadded:: 1.1

    Change chromatic pitch-class number to chromatic pitch-class name with flats::

        abjad> for n in range(13):
        ...     pc = n / 2.0
        ...     name = pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_flats(pc)
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

    .. versionchanged:: 2.0
        renamed ``pitchtools.pc_to_pitch_name_flats()`` to
        ``pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_flats()``.
    '''

    try:
        return _pitch_class_name_to_pitch_class_number_flats[chromatic_pitch_class_number]
    except KeyError:
        return _pitch_class_name_to_pitch_class_number_flats[abs(chromatic_pitch_class_number)]


_pitch_class_name_to_pitch_class_number_flats = {
        0:  'c',     0.5: 'dtqf',    1: 'df',    1.5:  'dqf',
        2:  'd',     2.5: 'etqf',    3: 'ef',    3.5:  'eqf',
        4:  'e',     4.5: 'fqf',     5: 'f',     5.5:  'gtqf',
        6:  'gf',    6.5: 'gqf',     7: 'g',     7.5:  'atqf',
        8:  'af',    8.5: 'aqf',     9: 'a',     9.5:  'btqf',
        10: 'bf',   10.5: 'bqf',    11: 'b',    11.5:  'cqf' }
