# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_Spanner___in___01():
    r'''Spanner containment tests components.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    beam = Beam()
    attach(beam, voice[1][:])

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8
                d'8
            }
            {
                e'8 [
                f'8 ]
            }
            {
                g'8
                a'8
            }
        }
        '''
        )

    assert voice[1] not in beam
    assert voice[1][0] in beam
    assert voice[1][1] in beam