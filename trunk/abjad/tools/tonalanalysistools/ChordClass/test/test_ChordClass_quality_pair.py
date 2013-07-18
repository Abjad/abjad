from abjad import *
from abjad.tools import tonalanalysistools


def test_ChordClass_quality_pair_01():

    cc = tonalanalysistools.ChordClass('c', 'major', 'triad', 'root')
    assert cc.quality_pair == ('major', 'triad')

    cc = tonalanalysistools.ChordClass('c', 'minor', 'triad', 'root')
    assert cc.quality_pair == ('minor', 'triad')


def test_ChordClass_quality_pair_02():

    cc = tonalanalysistools.ChordClass('c', 'dominant', 'seventh', 'root')
    assert cc.quality_pair == ('dominant', 'seventh')

    cc = tonalanalysistools.ChordClass('c', 'diminished', 'seventh', 'root')
    assert cc.quality_pair == ('diminished', 'seventh')
