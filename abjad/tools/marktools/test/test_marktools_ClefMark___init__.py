# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_marktools_ClefMark___init___01():

    clef_1 = marktools.ClefMark('treble')
    clef_2 = marktools.ClefMark(clef_1)

    assert clef_1 == clef_2
    assert not clef_1 is clef_2


def test_marktools_ClefMark___init___02():

    assert pytest.raises(TypeError, 'marktools.ClefMark(1)')
