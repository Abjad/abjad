from abjad.tools.pitchtools.MelodicChromaticIntervalSegment import MelodicChromaticIntervalSegment
from abjad.tools.pitchtools._ChromaticPitch import _ChromaticPitch


def transpose_chromatic_pitch_by_melodic_chromatic_interval_segment(pitch, segment):
    '''.. versionadded:: 2.0

    Transpose chromatic `pitch` by melodic chromatic interval `segment`::

        abjad> ncp = pitchtools.NumberedChromaticPitch(0)
        abjad> mcis = pitchtools.MelodicChromaticIntervalSegment([0, -1, 2])
        abjad> pitchtools.transpose_chromatic_pitch_by_melodic_chromatic_interval_segment(ncp, mcis)
        [NumberedChromaticPitch(0), NumberedChromaticPitch(-1), NumberedChromaticPitch(1)]

    Transpose by each interval in `segment` such that each tranposition
    transposes the resulting pitch of the previous transposition.

    Return list of numbered chromatic pitches.
    '''

    if not isinstance(pitch, _ChromaticPitch):
        raise TypeError

    if not isinstance(segment, MelodicChromaticIntervalSegment):
        raise TypeError

    if not hasattr(pitch, 'transpose'):
        pitch = pitch.numbered_chromatic_pitch
    pitches = [pitch.transpose(segment[0].number)]
    for interval in segment[1:]:
        pitches.append(pitches[-1].transpose(interval.number))
    return pitches
