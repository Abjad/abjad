# -*- encoding: utf-8 -*-
from abjad import *


def test_FixedDurationTuplet_preferred_duration_01():

    t = tuplettools.FixedDurationTuplet(Duration(4, 8), "c'8 d'8 e'8 f'8 g'8 a'8")
    t.preferred_denominator = 4

    r'''
    \times 4/6 {
        c'8
        d'8
        e'8
        f'8
        g'8
        a'8
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \times 4/6 {
            c'8
            d'8
            e'8
            f'8
            g'8
            a'8
        }
        '''
        )
