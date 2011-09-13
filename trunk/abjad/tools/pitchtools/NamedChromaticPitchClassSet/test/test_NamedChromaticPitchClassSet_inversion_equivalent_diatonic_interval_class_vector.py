from abjad import *


def test_NamedChromaticPitchClassSet_inversion_equivalent_diatonic_interval_class_vector_01():

    npcset = pitchtools.NamedChromaticPitchClassSet(['c', 'e', 'g', 'b'])
    dicv = npcset.inversion_equivalent_diatonic_interval_class_vector

    "DiatonicIntervalClassVector(P1: 0, aug1: 0, m2: 1, M2: 0, aug2: 0, dim3: 0, m3: 1, M3: 2, dim4: 0, P4: 2, aug4: 0)"

    assert dicv == pitchtools.InversionEquivalentDiatonicIntervalClassVector([
        pitchtools.NamedChromaticPitch('c', 4), pitchtools.NamedChromaticPitch('e', 4), pitchtools.NamedChromaticPitch('g', 4), pitchtools.NamedChromaticPitch('b', 4)])
