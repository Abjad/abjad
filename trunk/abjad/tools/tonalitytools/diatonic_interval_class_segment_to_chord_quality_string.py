from abjad.tools import pitchtools


def diatonic_interval_class_segment_to_chord_quality_string(dic_seg):
    '''.. versionadded:: 2.0

    Change diatonic interval-class segment `dic_seg` to chord quality string::

        abjad> from abjad.tools import tonalitytools

    ::

        abjad> dic_seg = pitchtools.InversionEquivalentDiatonicIntervalClassSegment([
        ...   pitchtools.InversionEquivalentDiatonicIntervalClass('major', 3),
        ...   pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 3),])
        abjad> tonalitytools.diatonic_interval_class_segment_to_chord_quality_string(dic_seg)
        'major'

    .. todo::
        Implement ``diatonic_interval_class_set_to_chord_quality_string()``.
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
        repr(pitchtools.InversionEquivalentDiatonicIntervalClassSegment([
            pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 3),
            pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 3),])): 'diminished',
        repr(pitchtools.InversionEquivalentDiatonicIntervalClassSegment([
            pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 3),
            pitchtools.InversionEquivalentDiatonicIntervalClass('major', 3),])): 'minor',
        repr(pitchtools.InversionEquivalentDiatonicIntervalClassSegment([
            pitchtools.InversionEquivalentDiatonicIntervalClass('major', 3),
            pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 3),])): 'major',
        repr(pitchtools.InversionEquivalentDiatonicIntervalClassSegment([
            pitchtools.InversionEquivalentDiatonicIntervalClass('major', 3),
            pitchtools.InversionEquivalentDiatonicIntervalClass('major', 3),])): 'augmented',
        # seventh chords
        repr(pitchtools.InversionEquivalentDiatonicIntervalClassSegment([
            pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 3),
            pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 3),
            pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 3),])): 'diminished',
        repr(pitchtools.InversionEquivalentDiatonicIntervalClassSegment([
            pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 3),
            pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 3),
            pitchtools.InversionEquivalentDiatonicIntervalClass('major', 3),])): 'half diminished',
        repr(pitchtools.InversionEquivalentDiatonicIntervalClassSegment([
            pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 3),
            pitchtools.InversionEquivalentDiatonicIntervalClass('major', 3),
            pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 3),])): 'minor',
        repr(pitchtools.InversionEquivalentDiatonicIntervalClassSegment([
            pitchtools.InversionEquivalentDiatonicIntervalClass('major', 3),
            pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 3),
            pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 3),])): 'dominant',
        repr(pitchtools.InversionEquivalentDiatonicIntervalClassSegment([
            pitchtools.InversionEquivalentDiatonicIntervalClass('major', 3),
            pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 3),
            pitchtools.InversionEquivalentDiatonicIntervalClass('major', 3),])): 'major',
        # ninth chords
        repr(pitchtools.InversionEquivalentDiatonicIntervalClassSegment([
            pitchtools.InversionEquivalentDiatonicIntervalClass('major', 3),
            pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 3),
            pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 3),
            pitchtools.InversionEquivalentDiatonicIntervalClass('major', 3),])): 'dominant',
        }

    try:
        quality_string = dic_seg_to_quality_string[repr(dic_seg)]
    except KeyError:
        raise TonalHarmonyError('unknown diatonic interval-class segment: %s' % str(dic_seg))

    return quality_string
