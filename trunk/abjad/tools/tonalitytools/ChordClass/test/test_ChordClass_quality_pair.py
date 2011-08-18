from abjad import *
from abjad.tools import tonalitytools


def test_ChordClass_quality_pair_01():

    cc = tonalitytools.ChordClass('c', 'major', 'triad', 'root')
    assert cc.quality_pair == ('major', 'triad')

    cc = tonalitytools.ChordClass('c', 'minor', 'triad', 'root')
    assert cc.quality_pair == ('minor', 'triad')


def test_ChordClass_quality_pair_02():

    cc = tonalitytools.ChordClass('c', 'dominant', 'seventh', 'root')
    assert cc.quality_pair == ('dominant', 'seventh')

    cc = tonalitytools.ChordClass('c', 'diminished', 'seventh', 'root')
    assert cc.quality_pair == ('diminished', 'seventh')
