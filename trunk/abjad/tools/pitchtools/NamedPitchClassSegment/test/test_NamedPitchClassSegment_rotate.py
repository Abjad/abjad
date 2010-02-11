from abjad import *


def test_NamedPitchClassSegment_rotate_01( ):

   npc_segment_1 = pitchtools.NamedPitchClassSegment([
      pitchtools.NamedPitchClass('c'),
      pitchtools.NamedPitchClass('d'),
      pitchtools.NamedPitchClass('e'),
      pitchtools.NamedPitchClass('f'),
      pitchtools.NamedPitchClass('g'),])

   npc_segment_2 = pitchtools.NamedPitchClassSegment([
      pitchtools.NamedPitchClass('g'),
      pitchtools.NamedPitchClass('c'),
      pitchtools.NamedPitchClass('d'),
      pitchtools.NamedPitchClass('e'),
      pitchtools.NamedPitchClass('f'),])

   assert npc_segment_1.rotate(1) == npc_segment_2
   assert npc_segment_1.rotate(-4) == npc_segment_2
   assert npc_segment_2.rotate(-1) == npc_segment_1
   assert npc_segment_2.rotate(4) == npc_segment_1
