# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_Spanner_start_offset_01():
    r'''Returns start time of spanner in score.
    '''

    container = Container("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, container[1:3])
    glissando = spannertools.Glissando()
    attach(glissando, container[:])

    assert format(container) == stringtools.normalize(
        r'''
        {
            c'8 \glissando
            d'8 [ \glissando
            e'8 ] \glissando
            f'8
        }
        '''
        )

    assert inspect_(beam).get_timespan().start_offset == Duration(1, 8)
    assert inspect_(glissando).get_timespan().start_offset == Duration(0)