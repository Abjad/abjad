from abjad.tools import sequencetools


def harmonic_chromatic_interval_class_number_dictionary(pitches):
    '''.. versionadded:: 1.1

    Change named chromatic pitches to harmonic chromatic interval-class number dictionary::

        >>> chord = Chord([0, 2, 11], (1, 4))
        >>> vector = pitchtools.harmonic_chromatic_interval_class_number_dictionary(
        ... chord.written_pitches)
        >>> vector
        {0: 0, 1: 0, 2: 1, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 1, 10: 0, 11: 1}

    Return dictionary.

    .. versionchanged:: 2.0
        renamed ``pitchtools.get_interval_vector()`` to
        ``pitchtools.harmonic_chromatic_interval_class_number_dictionary()``.
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
        intervals.append(interval)

    vector = {}

    for i in range(12):
        vector[i] = intervals.count(i)

    return vector
