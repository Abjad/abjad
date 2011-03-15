from abjad.tools.pitchtools.MelodicChromaticIntervalSegment import MelodicChromaticIntervalSegment
from abjad.tools.pitchtools._ChromaticPitch import _ChromaticPitch


def transpose_chromatic_pitch_by_melodic_chromatic_interval_segment(pitch, segment):
   '''Transpose `pitch` by each interval in `segment`, such that each transposition
   transposes the resulting pitch of the previous transposition.

      abjad> ncp = NumberedChromaticPitch(0)
      abjad> mcis = MelodicChromaticIntervalSegment([0, -1, 2])
      abjad> transpose_chromatic_pitch_by_melodic_chromatic_interval_segment(ncp, mcis)
      [NumberedChromaticPitch(0), NumberedChromaticPitch(-1), NumberedChromaticPitch(1)]

   '''

   assert isinstance(pitch, _ChromaticPitch)
   assert isinstance(segment, MelodicChromaticIntervalSegment)
   if not hasattr(pitch, 'transpose'):
      pitch = pitch.numbered_chromatic_pitch
   pitches = [pitch.transpose(segment[0].number)]
   for interval in segment[1:]:
      pitches.append(pitches[-1].transpose(interval.number))
   return pitches
