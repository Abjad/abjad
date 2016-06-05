# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_make_skips_01():

    durations = [(1, 2), (1, 3), (1, 4), (1, 5)]
    durations = [Duration(*x) for x in durations]
    staff = Staff(scoretools.make_skips(Duration(1, 4), durations))

    r'''
    \new Staff {
        s4 * 2
        s4 * 4/3
        s4 * 1
        s4 * 4/5
    }
    '''

    assert inspect_(staff).is_well_formed()
    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            s4 * 2
            s4 * 4/3
            s4 * 1
            s4 * 4/5
        }
        '''
        )
