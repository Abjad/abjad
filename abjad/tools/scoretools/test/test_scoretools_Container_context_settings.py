# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Container_context_settings_01():
    r'''Noncontext containers bracket context settings at opening.
    '''

    container = Container("c'8 d'8 e'8 f'8")
    set_(container).score.beam_exceptions = schemetools.SchemeVector()

    assert format(container) == stringtools.normalize(
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
