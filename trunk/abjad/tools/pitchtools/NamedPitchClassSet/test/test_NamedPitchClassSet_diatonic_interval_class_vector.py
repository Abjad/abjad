from abjad import *


def test_NamedPitchClassSet_diatonic_interval_class_vector_01( ):

   npcset = pitchtools.NamedPitchClassSet(['c', 'e', 'g', 'b'])
   dicv = npcset.diatonic_interval_class_vector

   "DiatonicIntervalClassVector(P1: 0, aug1: 0, m2: 1, M2: 0, aug2: 0, dim3: 0, m3: 1, M3: 2, dim4: 0, P4: 2, aug4: 0)"

   assert dicv == pitchtools.InversionEquivalentDiatonicIntervalClassVector([
      pitchtools.NamedPitch('c', 4), pitchtools.NamedPitch('e', 4), pitchtools.NamedPitch('g', 4), pitchtools.NamedPitch('b', 4)])
