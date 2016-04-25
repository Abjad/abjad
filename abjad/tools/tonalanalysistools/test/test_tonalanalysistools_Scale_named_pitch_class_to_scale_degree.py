# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_Scale_named_pitch_class_to_scale_degree_01():

    scale = tonalanalysistools.Scale('c', 'major')

    assert scale.named_pitch_class_to_scale_degree('c') == \
        tonalanalysistools.ScaleDegree(1)
    assert scale.named_pitch_class_to_scale_degree('d') == \
        tonalanalysistools.ScaleDegree(2)
    assert scale.named_pitch_class_to_scale_degree('e') == \
        tonalanalysistools.ScaleDegree(3)
    assert scale.named_pitch_class_to_scale_degree('f') == \
        tonalanalysistools.ScaleDegree(4)
    assert scale.named_pitch_class_to_scale_degree('g') == \
        tonalanalysistools.ScaleDegree(5)
    assert scale.named_pitch_class_to_scale_degree('a') == \
        tonalanalysistools.ScaleDegree(6)
    assert scale.named_pitch_class_to_scale_degree('b') == \
        tonalanalysistools.ScaleDegree(7)


def test_tonalanalysistools_Scale_named_pitch_class_to_scale_degree_02():

    scale = tonalanalysistools.Scale('c', 'major')

    assert scale.named_pitch_class_to_scale_degree('cf') == \
        tonalanalysistools.ScaleDegree('flat', 1)
    assert scale.named_pitch_class_to_scale_degree('df') == \
        tonalanalysistools.ScaleDegree('flat', 2)
    assert scale.named_pitch_class_to_scale_degree('ef') == \
        tonalanalysistools.ScaleDegree('flat', 3)
    assert scale.named_pitch_class_to_scale_degree('ff') == \
        tonalanalysistools.ScaleDegree('flat', 4)
    assert scale.named_pitch_class_to_scale_degree('gf') == \
        tonalanalysistools.ScaleDegree('flat', 5)
    assert scale.named_pitch_class_to_scale_degree('af') == \
        tonalanalysistools.ScaleDegree('flat', 6)
    assert scale.named_pitch_class_to_scale_degree('bf') == \
        tonalanalysistools.ScaleDegree('flat', 7)


def test_tonalanalysistools_Scale_named_pitch_class_to_scale_degree_03():

    scale = tonalanalysistools.Scale('c', 'major')

    assert scale.named_pitch_class_to_scale_degree('cs') == \
        tonalanalysistools.ScaleDegree('sharp', 1)
    assert scale.named_pitch_class_to_scale_degree('ds') == \
        tonalanalysistools.ScaleDegree('sharp', 2)
    assert scale.named_pitch_class_to_scale_degree('es') == \
        tonalanalysistools.ScaleDegree('sharp', 3)
    assert scale.named_pitch_class_to_scale_degree('fs') == \
        tonalanalysistools.ScaleDegree('sharp', 4)
    assert scale.named_pitch_class_to_scale_degree('gs') == \
        tonalanalysistools.ScaleDegree('sharp', 5)
    assert scale.named_pitch_class_to_scale_degree('as') == \
        tonalanalysistools.ScaleDegree('sharp', 6)
    assert scale.named_pitch_class_to_scale_degree('bs') == \
        tonalanalysistools.ScaleDegree('sharp', 7)
