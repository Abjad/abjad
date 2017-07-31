# -*- coding: utf-8 -*-
import abjad
from abjad.tools import rhythmtreetools


def test_rhythmtreetools_RhythmTreeNode___call___01():

    rtm = '(1 (1 1 1 1))'
    tree = rhythmtreetools.RhythmTreeParser()(rtm)[0]
    result = tree((1, 4))

    assert isinstance(result, abjad.Selection)
    assert len(result) == 4
    assert all(isinstance(x, abjad.Note) for x in result)
    assert all(x.written_duration == abjad.Duration(1, 16) for x in result)


def test_rhythmtreetools_RhythmTreeNode___call___02():

    rtm = '(1 (1 (2 (1 1 1)) 2))'
    tree = rhythmtreetools.RhythmTreeParser()(rtm)[0]
    result = tree((1, 4))

    assert isinstance(result, list)
    assert len(result) == 1
    assert format(result[0]) == abjad.String.normalize(
        r'''
        \times 4/5 {
            c'16
            \times 2/3 {
                c'16
                c'16
                c'16
            }
            c'8
        }
        '''
        )


def test_rhythmtreetools_RhythmTreeNode___call___03():

    rtm = '(1 (1 (2 (1 (2 (1 1)) 1)) 2))'
    tree = rhythmtreetools.RhythmTreeParser()(rtm)[0]
    result = tree((1, 4))

    assert format(result[0]) == abjad.String.normalize(
        r'''
        \times 4/5 {
            c'16
            c'32
            c'32
            c'32
            c'32
            c'8
        }
        '''
        )
