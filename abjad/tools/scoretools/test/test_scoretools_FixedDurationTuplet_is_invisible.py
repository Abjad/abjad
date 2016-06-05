from abjad import *


def test_scoretools_FixedDurationTuplet_is_invisible_01():

    tuplet = scoretools.FixedDurationTuplet(Duration(1, 4), "c'8 c'8 c'8")

    assert format(tuplet) == stringtools.normalize(
        r'''
        \times 2/3 {
            c'8
            c'8
            c'8
        }
        '''
        )

    tuplet.is_invisible = True

    assert format(tuplet) == stringtools.normalize(
        r'''
        \scaleDurations #'(2 . 3) {
            c'8
            c'8
            c'8
        }
        '''
        )

    tuplet.is_invisible = False

    assert format(tuplet) == stringtools.normalize(
        r'''
        \times 2/3 {
            c'8
            c'8
            c'8
        }
        '''
        )
