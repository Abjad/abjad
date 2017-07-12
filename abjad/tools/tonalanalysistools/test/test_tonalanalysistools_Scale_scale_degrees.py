# -*- coding: utf-8 -*-
import abjad
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_Scale_scale_degrees_01():

    scale = tonalanalysistools.Scale('g', 'major')

    assert scale.tonic == abjad.NamedPitchClass('g')
    assert scale.superdominant == abjad.NamedPitchClass('a')
    assert scale.mediant == abjad.NamedPitchClass('b')
    assert scale.subdominant == abjad.NamedPitchClass('c')
    assert scale.dominant == abjad.NamedPitchClass('d')
    assert scale.submediant == abjad.NamedPitchClass('e')
    assert scale.leading_tone == abjad.NamedPitchClass('fs')
