from abjad.tools import sequencetools


def inversion_equivalent_chromatic_interval_class_number_dictionary(pitches):
    r'''.. versionadded:: 1.1

    Change named chromatic `pitches` to inversion-equivalent chromatic interval-class number
    dictionary::

        >>> chord = Chord("<c' d' b''>4")
        >>> vector = pitchtools.inversion_equivalent_chromatic_interval_class_number_dictionary(
        ... chord.written_pitches)
        >>> for i in range(7):
        ...     print '\t%s\t%s' % (i, vector[i])
        ...
            0  0
            1  1
            2  1
            3  1
            4  0
            5  0
            6  0

    .. versionchanged:: 2.0
        works with quartertones.

    Return dictionary.
    '''
    from abjad.tools import pitchtools

    numbers = []

    for pitch in pitches:
        if not isinstance(pitch, pitchtools.NamedChromaticPitch):
            raise ValueError
        numbers.append(pitch.numbered_chromatic_pitch._chromatic_pitch_number)

    pairs = sequencetools.yield_all_unordered_pairs_of_sequence(numbers)

    intervals = []

    for pair in pairs:
        interval = max(pair) - min(pair)
        interval %= 12
        if 6 < interval:
            interval = 12 - interval
        intervals.append(interval)

    vector = {}

    # 12-ET pitches only
    if all([isinstance(interval, int) for interval in intervals]):
        for i in range(7):
            vector[i] = intervals.count(i)
    # 24-ET pitches included
    else:
        for i in range(13):
            if i % 2 == 0:
                key = i / 2
            else:
                key = i / 2.0
            vector[key] = intervals.count(key)

    return vector
