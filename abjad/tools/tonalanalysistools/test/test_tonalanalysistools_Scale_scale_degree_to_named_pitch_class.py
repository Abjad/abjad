# -*- coding: utf-8 -*-
import abjad
import pytest
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_Scale_scale_degree_to_named_pitch_class_01():

    scale = tonalanalysistools.Scale('c', 'major')

    assert scale.scale_degree_to_named_pitch_class(1) == \
        abjad.NamedPitchClass('c')
    assert scale.scale_degree_to_named_pitch_class(2) == \
        abjad.NamedPitchClass('d')
    assert scale.scale_degree_to_named_pitch_class(3) == \
        abjad.NamedPitchClass('e')
    assert scale.scale_degree_to_named_pitch_class(4) == \
        abjad.NamedPitchClass('f')
    assert scale.scale_degree_to_named_pitch_class(5) == \
        abjad.NamedPitchClass('g')
    assert scale.scale_degree_to_named_pitch_class(6) == \
        abjad.NamedPitchClass('a')
    assert scale.scale_degree_to_named_pitch_class(7) == \
        abjad.NamedPitchClass('b')


def test_tonalanalysistools_Scale_scale_degree_to_named_pitch_class_02():

    scale = tonalanalysistools.Scale('c', 'major')

    assert scale.scale_degree_to_named_pitch_class('flat', 1) == \
        abjad.NamedPitchClass('cf')
    assert scale.scale_degree_to_named_pitch_class('flat', 2) == \
        abjad.NamedPitchClass('df')
    assert scale.scale_degree_to_named_pitch_class('flat', 3) == \
        abjad.NamedPitchClass('ef')
    assert scale.scale_degree_to_named_pitch_class('flat', 4) == \
        abjad.NamedPitchClass('ff')
    assert scale.scale_degree_to_named_pitch_class('flat', 5) == \
        abjad.NamedPitchClass('gf')
    assert scale.scale_degree_to_named_pitch_class('flat', 6) == \
        abjad.NamedPitchClass('af')
    assert scale.scale_degree_to_named_pitch_class('flat', 7) == \
        abjad.NamedPitchClass('bf')


def test_tonalanalysistools_Scale_scale_degree_to_named_pitch_class_03():

    scale = tonalanalysistools.Scale('c', 'major')

    assert scale.scale_degree_to_named_pitch_class('sharp', 1) == \
        abjad.NamedPitchClass('cs')
    assert scale.scale_degree_to_named_pitch_class('sharp', 2) == \
        abjad.NamedPitchClass('ds')
    assert scale.scale_degree_to_named_pitch_class('sharp', 3) == \
        abjad.NamedPitchClass('es')
    assert scale.scale_degree_to_named_pitch_class('sharp', 4) == \
        abjad.NamedPitchClass('fs')
    assert scale.scale_degree_to_named_pitch_class('sharp', 5) == \
        abjad.NamedPitchClass('gs')
    assert scale.scale_degree_to_named_pitch_class('sharp', 6) == \
        abjad.NamedPitchClass('as')
    assert scale.scale_degree_to_named_pitch_class('sharp', 7) == \
        abjad.NamedPitchClass('bs')


def test_tonalanalysistools_Scale_scale_degree_to_named_pitch_class_04():

    scale = tonalanalysistools.Scale('c', 'major')

    assert pytest.raises(ValueError,
        'scale.scale_degree_to_named_pitch_class(99)')
