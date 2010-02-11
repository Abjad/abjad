from abjad import *


def test_NamedPitchClassSegment_retrograde_01( ):

   npc_segment_1 = pitchtools.NamedPitchClassSegment([
      pitchtools.NamedPitchClass('c'),
      pitchtools.NamedPitchClass('d'),
      pitchtools.NamedPitchClass('e'),
      pitchtools.NamedPitchClass('f'),
      pitchtools.NamedPitchClass('g'),])

   npc_segment_2 = pitchtools.NamedPitchClassSegment([
      pitchtools.NamedPitchClass('g'),
      pitchtools.NamedPitchClass('f'),
      pitchtools.NamedPitchClass('e'),
      pitchtools.NamedPitchClass('d'),
      pitchtools.NamedPitchClass('c'),])

   assert npc_segment_1.retrograde( ) == npc_segment_2
   assert npc_segment_2.retrograde( ) == npc_segment_1
