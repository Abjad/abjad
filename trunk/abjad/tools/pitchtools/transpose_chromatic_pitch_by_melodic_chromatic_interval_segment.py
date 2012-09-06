def transpose_chromatic_pitch_by_melodic_chromatic_interval_segment(pitch, segment):
    '''.. versionadded:: 2.0

    Transpose chromatic `pitch` by melodic chromatic interval `segment`::

        >>> ncp = pitchtools.NumberedChromaticPitch(0)
        >>> mcis = pitchtools.MelodicChromaticIntervalSegment([0, -1, 2])
        >>> pitchtools.transpose_chromatic_pitch_by_melodic_chromatic_interval_segment(ncp, mcis)
        [NumberedChromaticPitch(0), NumberedChromaticPitch(-1), NumberedChromaticPitch(1)]

    Transpose by each interval in `segment` such that each tranposition
    transposes the resulting pitch of the previous transposition.

    Return list of numbered chromatic pitches.
    '''
    from abjad.tools import pitchtools

    # check input
    if not isinstance(pitch, pitchtools.ChromaticPitchObject):
        raise TypeError

    # check input
    if not isinstance(segment, pitchtools.MelodicChromaticIntervalSegment):
        raise TypeError

    if not hasattr(pitch, 'transpose'):
        pitch = pitch.numbered_chromatic_pitch

    pitches = [pitch.transpose(segment[0].number)]

    for interval in segment[1:]:
        pitches.append(pitches[-1].transpose(interval.number))

    return pitches
