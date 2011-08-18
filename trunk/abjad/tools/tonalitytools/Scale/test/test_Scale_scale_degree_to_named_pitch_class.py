from abjad import *
from abjad.tools import tonalitytools
import py.test


def test_Scale_scale_degree_to_named_pitch_class_01():

    scale = tonalitytools.Scale('c', 'major')

    assert scale.scale_degree_to_named_chromatic_pitch_class(1) == \
        pitchtools.NamedChromaticPitchClass('c')
    assert scale.scale_degree_to_named_chromatic_pitch_class(2) == \
        pitchtools.NamedChromaticPitchClass('d')
    assert scale.scale_degree_to_named_chromatic_pitch_class(3) == \
        pitchtools.NamedChromaticPitchClass('e')
    assert scale.scale_degree_to_named_chromatic_pitch_class(4) == \
        pitchtools.NamedChromaticPitchClass('f')
    assert scale.scale_degree_to_named_chromatic_pitch_class(5) == \
        pitchtools.NamedChromaticPitchClass('g')
    assert scale.scale_degree_to_named_chromatic_pitch_class(6) == \
        pitchtools.NamedChromaticPitchClass('a')
    assert scale.scale_degree_to_named_chromatic_pitch_class(7) == \
        pitchtools.NamedChromaticPitchClass('b')


def test_Scale_scale_degree_to_named_pitch_class_02():

    scale = tonalitytools.Scale('c', 'major')

    assert scale.scale_degree_to_named_chromatic_pitch_class('flat', 1) == \
        pitchtools.NamedChromaticPitchClass('cf')
    assert scale.scale_degree_to_named_chromatic_pitch_class('flat', 2) == \
        pitchtools.NamedChromaticPitchClass('df')
    assert scale.scale_degree_to_named_chromatic_pitch_class('flat', 3) == \
        pitchtools.NamedChromaticPitchClass('ef')
    assert scale.scale_degree_to_named_chromatic_pitch_class('flat', 4) == \
        pitchtools.NamedChromaticPitchClass('ff')
    assert scale.scale_degree_to_named_chromatic_pitch_class('flat', 5) == \
        pitchtools.NamedChromaticPitchClass('gf')
    assert scale.scale_degree_to_named_chromatic_pitch_class('flat', 6) == \
        pitchtools.NamedChromaticPitchClass('af')
    assert scale.scale_degree_to_named_chromatic_pitch_class('flat', 7) == \
        pitchtools.NamedChromaticPitchClass('bf')


def test_Scale_scale_degree_to_named_pitch_class_03():

    scale = tonalitytools.Scale('c', 'major')

    assert scale.scale_degree_to_named_chromatic_pitch_class('sharp', 1) == \
        pitchtools.NamedChromaticPitchClass('cs')
    assert scale.scale_degree_to_named_chromatic_pitch_class('sharp', 2) == \
        pitchtools.NamedChromaticPitchClass('ds')
    assert scale.scale_degree_to_named_chromatic_pitch_class('sharp', 3) == \
        pitchtools.NamedChromaticPitchClass('es')
    assert scale.scale_degree_to_named_chromatic_pitch_class('sharp', 4) == \
        pitchtools.NamedChromaticPitchClass('fs')
    assert scale.scale_degree_to_named_chromatic_pitch_class('sharp', 5) == \
        pitchtools.NamedChromaticPitchClass('gs')
    assert scale.scale_degree_to_named_chromatic_pitch_class('sharp', 6) == \
        pitchtools.NamedChromaticPitchClass('as')
    assert scale.scale_degree_to_named_chromatic_pitch_class('sharp', 7) == \
        pitchtools.NamedChromaticPitchClass('bs')


def test_Scale_scale_degree_to_named_pitch_class_04():

    scale = tonalitytools.Scale('c', 'major')

    assert py.test.raises(ValueError,
        'scale.scale_degree_to_named_chromatic_pitch_class(99)')
