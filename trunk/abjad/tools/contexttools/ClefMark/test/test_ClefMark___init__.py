from abjad import *
import py.test


def test_ClefMark___init___01():

    clef_1 = contexttools.ClefMark('treble')
    clef_2 = contexttools.ClefMark(clef_1)

    assert clef_1 == clef_2
    assert not clef_1 is clef_2


def test_ClefMark___init___02():

    assert py.test.raises(TypeError, 'contexttools.ClefMark(1)')
