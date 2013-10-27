# -*- encoding: utf-8 -*-
from abjad import *


def test_tuplettools_FixedDurationTuplet_preferred_denominator_01():

    tuplet = tuplettools.FixedDurationTuplet(Duration(4, 8), [])
    tuplet.extend("c'8 d'8 e'8 f'8 g'8 a'8")
    tuplet.preferred_denominator = 4

    assert testtools.compare(
        tuplet,
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

    assert inspect(tuplet).is_well_formed()
