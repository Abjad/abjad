# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_Scale_diatonic_interval_class_segment_01():

    scale = tonalanalysistools.Scale('a', 'major')
    dicg = scale.named_interval_class_segment

    assert str(dicg) == '<+M2, +M2, +m2, +M2, +M2, +M2, +m2>'


def test_tonalanalysistools_Scale_diatonic_interval_class_segment_02():

    scale = tonalanalysistools.Scale('a', 'dorian')
    dicg = scale.named_interval_class_segment

    assert str(dicg) == '<+M2, +m2, +M2, +M2, +M2, +m2, +M2>'
