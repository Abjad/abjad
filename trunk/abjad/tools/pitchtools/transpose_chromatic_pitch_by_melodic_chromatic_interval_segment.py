# -*- encoding: utf-8 -*-


def transpose_chromatic_pitch_by_melodic_chromatic_interval_segment(pitch, segment):
    '''Transpose chromatic `pitch` by melodic chromatic interval `segment`:

    ::

        >>> ncp = pitchtools.NumberedPitch(0)
        >>> mcis = pitchtools.MelodicChromaticIntervalSegment([0, -1, 2])
        >>> pitchtools.transpose_chromatic_pitch_by_melodic_chromatic_interval_segment(ncp, mcis)
        [NumberedPitch(0), NumberedPitch(-1), NumberedPitch(1)]

    Transpose by each interval in `segment` such that each tranposition
    transposes the resulting pitch of the previous transposition.

    Return list of numbered chromatic pitches.
    '''
    from abjad.tools import pitchtools

    # check input
    if not isinstance(pitch, (
        pitchtools.NumberedPitch,
        pitchtools.NamedPitch,
        )):
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
