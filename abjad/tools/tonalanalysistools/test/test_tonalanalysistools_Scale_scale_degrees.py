# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_Scale_scale_degrees_01():

    scale = tonalanalysistools.Scale('g', 'major')

    assert scale.tonic == pitchtools.NamedPitchClass('g')
    assert scale.superdominant == pitchtools.NamedPitchClass('a')
    assert scale.mediant == pitchtools.NamedPitchClass('b')
    assert scale.subdominant == pitchtools.NamedPitchClass('c')
    assert scale.dominant == pitchtools.NamedPitchClass('d')
    assert scale.submediant == pitchtools.NamedPitchClass('e')
    assert scale.leading_tone == pitchtools.NamedPitchClass('fs')
