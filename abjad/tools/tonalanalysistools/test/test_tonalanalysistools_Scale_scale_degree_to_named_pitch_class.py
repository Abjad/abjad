# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools
import pytest


def test_tonalanalysistools_Scale_scale_degree_to_named_pitch_class_01():

    scale = tonalanalysistools.Scale('c', 'major')

    assert scale.scale_degree_to_named_pitch_class(1) == \
        pitchtools.NamedPitchClass('c')
    assert scale.scale_degree_to_named_pitch_class(2) == \
        pitchtools.NamedPitchClass('d')
    assert scale.scale_degree_to_named_pitch_class(3) == \
        pitchtools.NamedPitchClass('e')
    assert scale.scale_degree_to_named_pitch_class(4) == \
        pitchtools.NamedPitchClass('f')
    assert scale.scale_degree_to_named_pitch_class(5) == \
        pitchtools.NamedPitchClass('g')
    assert scale.scale_degree_to_named_pitch_class(6) == \
        pitchtools.NamedPitchClass('a')
    assert scale.scale_degree_to_named_pitch_class(7) == \
        pitchtools.NamedPitchClass('b')


def test_tonalanalysistools_Scale_scale_degree_to_named_pitch_class_02():

    scale = tonalanalysistools.Scale('c', 'major')

    assert scale.scale_degree_to_named_pitch_class('flat', 1) == \
        pitchtools.NamedPitchClass('cf')
    assert scale.scale_degree_to_named_pitch_class('flat', 2) == \
        pitchtools.NamedPitchClass('df')
    assert scale.scale_degree_to_named_pitch_class('flat', 3) == \
        pitchtools.NamedPitchClass('ef')
    assert scale.scale_degree_to_named_pitch_class('flat', 4) == \
        pitchtools.NamedPitchClass('ff')
    assert scale.scale_degree_to_named_pitch_class('flat', 5) == \
        pitchtools.NamedPitchClass('gf')
    assert scale.scale_degree_to_named_pitch_class('flat', 6) == \
        pitchtools.NamedPitchClass('af')
    assert scale.scale_degree_to_named_pitch_class('flat', 7) == \
        pitchtools.NamedPitchClass('bf')


def test_tonalanalysistools_Scale_scale_degree_to_named_pitch_class_03():

    scale = tonalanalysistools.Scale('c', 'major')

    assert scale.scale_degree_to_named_pitch_class('sharp', 1) == \
        pitchtools.NamedPitchClass('cs')
    assert scale.scale_degree_to_named_pitch_class('sharp', 2) == \
        pitchtools.NamedPitchClass('ds')
    assert scale.scale_degree_to_named_pitch_class('sharp', 3) == \
        pitchtools.NamedPitchClass('es')
    assert scale.scale_degree_to_named_pitch_class('sharp', 4) == \
        pitchtools.NamedPitchClass('fs')
    assert scale.scale_degree_to_named_pitch_class('sharp', 5) == \
        pitchtools.NamedPitchClass('gs')
    assert scale.scale_degree_to_named_pitch_class('sharp', 6) == \
        pitchtools.NamedPitchClass('as')
    assert scale.scale_degree_to_named_pitch_class('sharp', 7) == \
        pitchtools.NamedPitchClass('bs')


def test_tonalanalysistools_Scale_scale_degree_to_named_pitch_class_04():

    scale = tonalanalysistools.Scale('c', 'major')

    assert pytest.raises(ValueError,
        'scale.scale_degree_to_named_pitch_class(99)')
