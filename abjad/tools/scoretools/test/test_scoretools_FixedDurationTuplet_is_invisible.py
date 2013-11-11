from abjad import *


def test_scoretools_FixedDurationTuplet_is_invisible_01():

    tuplet = scoretools.FixedDurationTuplet(Duration(1, 4), "c'8 c'8 c'8")

    assert systemtools.TestManager.compare(
        tuplet,
        r'''
        \times 2/3 {
            c'8
            c'8
            c'8
        }
        '''
        )

    tuplet.is_invisible = True

    assert systemtools.TestManager.compare(
        tuplet,
        r'''
        \scaleDurations #'(2 . 3) {
            c'8
            c'8
            c'8
        }
        '''
        )

    tuplet.is_invisible = False

    assert systemtools.TestManager.compare(
        tuplet,
        r'''
        \times 2/3 {
            c'8
            c'8
            c'8
        }
        '''
        )
