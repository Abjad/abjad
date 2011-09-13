from abjad.tools import sequencetools
from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch


def named_chromatic_pitches_to_inversion_equivalent_chromatic_interval_class_number_dictionary(
    pitches):
    r'''.. versionadded:: 1.1

    Change named chromatic `pitches` to inversion-equivalent chromatic interval-class number
    dictionary::

        abjad> chord = Chord([0, 2, 11], (1, 4))
        abjad> vector = pitchtools.named_chromatic_pitches_to_inversion_equivalent_chromatic_interval_class_number_dictionary(chord.written_pitches)
        abjad> for i in range(7):
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

    .. versionchanged:: 2.0
        renamed ``pitchtools.get_interval_class_vector()`` to
        ``pitchtools.named_chromatic_pitches_to_inversion_equivalent_chromatic_interval_class_number_dictionary()``.
    '''

    numbers = []

    for pitch in pitches:
        if not isinstance(pitch, NamedChromaticPitch):
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
