# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_FixedDurationTuplet_preferred_denominator_01():

    tuplet = scoretools.FixedDurationTuplet(Duration(4, 8), [])
    tuplet.extend("c'8 d'8 e'8 f'8 g'8 a'8")
    tuplet.preferred_denominator = 4

    assert format(tuplet) == stringtools.normalize(
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

    assert inspect_(tuplet).is_well_formed()
