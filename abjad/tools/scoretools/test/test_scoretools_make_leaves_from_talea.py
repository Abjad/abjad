# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_make_leaves_from_talea_01():

    leaves = scoretools.make_leaves_from_talea([3, -3, 5, -5], 8)
    staff = Staff(leaves)

    r'''
    \new Staff {
      c'4.
      r4.
      c'2 ~
      c'8
      r2
      r8
    }
    '''

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'4.
            r4.
            c'2 ~
            c'8
            r2
            r8
        }
        '''
        )
