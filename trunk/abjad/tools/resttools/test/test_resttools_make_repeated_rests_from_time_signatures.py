# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import sequencetools


def test_resttools_make_repeated_rests_from_time_signatures_01():
    r'''Make repeated rests from list of integer pairs.
    '''

    rests = resttools.make_repeated_rests_from_time_signatures([(2, 8), (3, 32)])
    assert len(rests) == 2

    rests = sequencetools.flatten_sequence(rests)
    staff = Staff(rests)

    r'''
    \new Staff {
        r8
        r8
        r32
        r32
        r32
    }
    '''

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            r8
            r8
            r32
            r32
            r32
        }
        '''
        )
    assert select(staff).is_well_formed()
