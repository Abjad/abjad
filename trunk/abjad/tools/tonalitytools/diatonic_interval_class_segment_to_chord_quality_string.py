def diatonic_interval_class_segment_to_chord_quality_string(dic_seg):
    '''Change diatonic interval-class segment to chord quality string:

    ::

        >>> dic_seg = pitchtools.InversionEquivalentDiatonicIntervalClassSegment([
        ...   pitchtools.InversionEquivalentDiatonicIntervalClass('major', 3),
        ...   pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 3),])
        >>> tonalitytools.diatonic_interval_class_segment_to_chord_quality_string(dic_seg)
        'major'

    '''

    # Note: the repeated calls to repr() in the implementation of
    #         this function accommodate the fact that the Abjad
    #         DiatonicIntervalClassSegment inherits from the built-in
    #         Python list class, which is mutable and designed to
    #         to be unhashable, ie, not used as the key to a dictionary.
    #         Since repr() returns a string and since the repr()
    #         of different DiatonicIntervalClassSegments are guaranteed
    #         to be unique based on value, storing reprs as dictionary
    #         keys works fine.
    dic_seg_to_quality_string = {
        # triads
        '<m3, m3>': 'diminished',
        '<m3, M3>': 'minor',
        '<M3, m3>': 'major',
        '<M3, M3>': 'augmented',
        # seventh chords
        '<m3, m3, m3>': 'diminished',
        '<m3, m3, M3>': 'half diminished',
        '<m3, M3, m3>': 'minor',
        '<M3, m3, m3>': 'dominant',
        '<M3, m3, M3>': 'major',
        # ninth chords
        '<M3, m3, m3, M3>': 'dominant',
        }

    try:
        quality_string = dic_seg_to_quality_string[str(dic_seg)]
    except KeyError:
        message = 'unknown diatonic interval-class segment: %s.'
        raise TonalHarmonyError(messaeg % dic_seg)

    return quality_string
