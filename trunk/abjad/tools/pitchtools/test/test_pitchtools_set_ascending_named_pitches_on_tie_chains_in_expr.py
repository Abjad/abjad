# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_set_ascending_named_pitches_on_tie_chains_in_expr_01():
    r'''Appictation works on tie chains.
    '''

    voice = Voice(notetools.make_notes(0, [(5, 32)] * 4))
    pitchtools.set_ascending_named_pitches_on_tie_chains_in_expr(voice)

    r'''
    \new Voice {
        c'8 ~
        c'32
        cs'8 ~
        cs'32
        d'8 ~
        d'32
        ef'8 ~
        ef'32
    }
    '''

    assert inspect(voice).is_well_formed()
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 ~
            c'32
            cs'8 ~
            cs'32
            d'8 ~
            d'32
            ef'8 ~
            ef'32
        }
        '''
        )
