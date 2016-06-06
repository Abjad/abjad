# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Tuplet_grob_override_01():
    r'''Tuplets bracket grob overrides at before and after slots.
    '''

    tuplet = Tuplet((2, 3), "c'8 d'8 e'8 f'8")
    override(tuplet).glissando.thickness = 3

    assert format(tuplet) == stringtools.normalize(
        r'''
        \override Glissando.thickness = #3
        \tweak edge-height #'(0.7 . 0)
        \times 2/3 {
            c'8
            d'8
            e'8
            f'8
        }
        \revert Glissando.thickness
        '''
        )
