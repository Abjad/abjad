# -*- encoding: utf-8 -*-
from abjad import *


def test_RhythmTreeContainer___call___01():

    rtm = '(1 (1 (2 (1 1 1)) 2))'
    tree = rhythmtreetools.RhythmTreeParser()(rtm)[0]
    result = tree((1, 4))

    assert isinstance(result, (list, selectiontools.SliceSelection))
    assert len(result) == 1

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

    assert testtools.compare(
        result[0],
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


def test_RhythmTreeContainer___call___02():

    rtm = '(1 (1 (2 (1 1 1 1)) 1))'
    tree = rhythmtreetools.RhythmTreeParser()(rtm)[0]
    result = tree((1, 4))

    assert isinstance(result, (list, selectiontools.SliceSelection))
    assert len(result) == 6
    assert [x.lilypond_format for x in result] == ["c'16", "c'32", "c'32", "c'32", "c'32", "c'16"]
