# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_Scale_scale_degrees_01():

    scale = tonalanalysistools.Scale('g', 'major')

    assert scale.tonic == pitchtools.NamedChromaticPitchClass('g')
    assert scale.superdominant == pitchtools.NamedChromaticPitchClass('a')
    assert scale.mediant == pitchtools.NamedChromaticPitchClass('b')
    assert scale.subdominant == pitchtools.NamedChromaticPitchClass('c')
    assert scale.dominant == pitchtools.NamedChromaticPitchClass('d')
    assert scale.submediant == pitchtools.NamedChromaticPitchClass('e')
    assert scale.leading_tone == pitchtools.NamedChromaticPitchClass('fs')
