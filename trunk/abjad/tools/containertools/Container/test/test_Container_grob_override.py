# -*- encoding: utf-8 -*-
from abjad import *


def test_Container_grob_override_01():
    r'''Noncontext containers bracket grob overrides at opening and closing.
    '''

    t = Container("c'8 d'8 e'8 f'8")
    t.override.glissando.thickness = 3

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

    assert testtools.compare(
        t.lilypond_format,
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
