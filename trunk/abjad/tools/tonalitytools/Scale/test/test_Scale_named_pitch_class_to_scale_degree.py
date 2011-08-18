from abjad import *
from abjad.tools import tonalitytools


def test_Scale_named_pitch_class_to_scale_degree_01():

    scale = tonalitytools.Scale('c', 'major')

    assert scale.named_chromatic_pitch_class_to_scale_degree('c') == \
        tonalitytools.ScaleDegree(1)
    assert scale.named_chromatic_pitch_class_to_scale_degree('d') == \
        tonalitytools.ScaleDegree(2)
    assert scale.named_chromatic_pitch_class_to_scale_degree('e') == \
        tonalitytools.ScaleDegree(3)
    assert scale.named_chromatic_pitch_class_to_scale_degree('f') == \
        tonalitytools.ScaleDegree(4)
    assert scale.named_chromatic_pitch_class_to_scale_degree('g') == \
        tonalitytools.ScaleDegree(5)
    assert scale.named_chromatic_pitch_class_to_scale_degree('a') == \
        tonalitytools.ScaleDegree(6)
    assert scale.named_chromatic_pitch_class_to_scale_degree('b') == \
        tonalitytools.ScaleDegree(7)


def test_Scale_named_pitch_class_to_scale_degree_02():

    scale = tonalitytools.Scale('c', 'major')

    assert scale.named_chromatic_pitch_class_to_scale_degree('cf') == \
        tonalitytools.ScaleDegree('flat', 1)
    assert scale.named_chromatic_pitch_class_to_scale_degree('df') == \
        tonalitytools.ScaleDegree('flat', 2)
    assert scale.named_chromatic_pitch_class_to_scale_degree('ef') == \
        tonalitytools.ScaleDegree('flat', 3)
    assert scale.named_chromatic_pitch_class_to_scale_degree('ff') == \
        tonalitytools.ScaleDegree('flat', 4)
    assert scale.named_chromatic_pitch_class_to_scale_degree('gf') == \
        tonalitytools.ScaleDegree('flat', 5)
    assert scale.named_chromatic_pitch_class_to_scale_degree('af') == \
        tonalitytools.ScaleDegree('flat', 6)
    assert scale.named_chromatic_pitch_class_to_scale_degree('bf') == \
        tonalitytools.ScaleDegree('flat', 7)


def test_Scale_named_pitch_class_to_scale_degree_03():

    scale = tonalitytools.Scale('c', 'major')

    assert scale.named_chromatic_pitch_class_to_scale_degree('cs') == \
        tonalitytools.ScaleDegree('sharp', 1)
    assert scale.named_chromatic_pitch_class_to_scale_degree('ds') == \
        tonalitytools.ScaleDegree('sharp', 2)
    assert scale.named_chromatic_pitch_class_to_scale_degree('es') == \
        tonalitytools.ScaleDegree('sharp', 3)
    assert scale.named_chromatic_pitch_class_to_scale_degree('fs') == \
        tonalitytools.ScaleDegree('sharp', 4)
    assert scale.named_chromatic_pitch_class_to_scale_degree('gs') == \
        tonalitytools.ScaleDegree('sharp', 5)
    assert scale.named_chromatic_pitch_class_to_scale_degree('as') == \
        tonalitytools.ScaleDegree('sharp', 6)
    assert scale.named_chromatic_pitch_class_to_scale_degree('bs') == \
        tonalitytools.ScaleDegree('sharp', 7)
