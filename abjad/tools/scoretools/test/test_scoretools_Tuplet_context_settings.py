# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Tuplet_context_settings_01():
    r'''Tuplet bracket context settings at before slot.
    '''

    tuplet = Tuplet((2, 3), "c'8 d'8 e'8 f'8")
    set_(tuplet).score.beam_exceptions = schemetools.SchemeVector()

    assert format(tuplet) == stringtools.normalize(
        r'''
        \set Score.beamExceptions = #'()
        \tweak edge-height #'(0.7 . 0)
        \times 2/3 {
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )
