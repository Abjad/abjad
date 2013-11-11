# -*- encoding: utf-8 -*-
from abjad import *


def test_scoretools_Container_grob_override_01():
    r'''Noncontext containers bracket grob overrides at opening and closing.
    '''

    container = Container("c'8 d'8 e'8 f'8")
    override(container).glissando.thickness = 3

    assert systemtools.TestManager.compare(
        container,
        r'''
        {
            \override Glissando #'thickness = #3
            c'8
            d'8
            e'8
            f'8
            \revert Glissando #'thickness
        }
        '''
        )
