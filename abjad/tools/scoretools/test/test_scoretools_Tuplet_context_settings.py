# -*- coding: utf-8 -*-
import abjad


def test_scoretools_Tuplet_context_settings_01():
    r'''Tuplet bracket context abjad.settings at before slot.
    '''

    tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8 f'8")
    abjad.setting(tuplet).score.beam_exceptions = abjad.SchemeVector()

    assert format(tuplet) == abjad.String.normalize(
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
