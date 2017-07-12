# -*- coding: utf-8 -*-
import abjad


def test_scoretools_Container_context_settings_01():
    r'''Noncontext containers bracket context abjad.settings at opening.
    '''

    container = abjad.Container("c'8 d'8 e'8 f'8")
    abjad.setting(container).score.beam_exceptions = abjad.SchemeVector()

    assert format(container) == abjad.String.normalize(
        r'''
        {
            \set Score.beamExceptions = #'()
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )
