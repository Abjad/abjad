from abjad import *


def test_NamedChromaticPitchClass_apply_accidental_01():

    pc = pitchtools.NamedChromaticPitchClass('cs')

    assert pc.apply_accidental('sharp') == pitchtools.NamedChromaticPitchClass('css')
    assert pc.apply_accidental('flat') == pitchtools.NamedChromaticPitchClass('c')
    assert pc.apply_accidental('natural') == pitchtools.NamedChromaticPitchClass('cs')
