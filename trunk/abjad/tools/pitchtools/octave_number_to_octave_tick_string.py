def octave_number_to_octave_tick_string(octave_number):
    r""".. versionadded:: 2.0

    Change `octave_number` to octave tick string::

        abjad> for octave_number in range(-1, 9):
        ...     print "%s\t%s" % (octave_number, pitchtools.octave_number_to_octave_tick_string(octave_number))
        ...
        -1 ,,,,
        0  ,,,
        1  ,,
        2  ,
        3
        4  '
        5  ''
        6  '''
        7  ''''
        8  '''''

    Raise type error on noninteger input.

    Return string.
    """

    if not isinstance(octave_number, (int, long, float)):
        raise TypeError('\n\tOctave number must be int: "%s".' % octave_number)

    if isinstance(octave_number, float):
        if not int(octave_number) == octave_number:
            raise TypeError('\n\tOctave number must equal to int: "%s".' % octave_number)
        else:
            octave_number = int(octave_number)

    if octave_number < 3:
        return (3 - octave_number) * ','
    elif octave_number == 3:
        return ''
    else:
        return (octave_number - 3) * "'"
