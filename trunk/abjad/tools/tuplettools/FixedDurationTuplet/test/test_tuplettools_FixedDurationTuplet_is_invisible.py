from abjad import *


def test_tuplettools_FixedDurationTuplet_is_invisible_01():

    tuplet = tuplettools.FixedDurationTuplet(Duration(1, 4), "c'8 c'8 c'8")

    assert testtools.compare(
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

    assert testtools.compare(
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

    assert testtools.compare(
        tuplet,
        r'''
        \times 2/3 {
            c'8
            c'8
            c'8
        }
        '''
        )
