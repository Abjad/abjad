# -*- encoding: utf-8 -*-
from abjad import *


def test_skiptools_make_skips_with_multiplied_durations_01():

    durations = [(1, 2), (1, 3), (1, 4), (1, 5)]
    durations = [Duration(*x) for x in durations]
    staff = Staff(skiptools.make_skips_with_multiplied_durations(Duration(1, 4), durations))

    r'''
    \new Staff {
        s4 * 2
        s4 * 4/3
        s4 * 1
        s4 * 4/5
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            s4 * 2
            s4 * 4/3
            s4 * 1
            s4 * 4/5
        }
        '''
        )
