# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_Spanner_stop_offset_01():
    r'''Returns stop time of spanner in score.
    '''

    container = Container("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, container[1:3])
    glissando = spannertools.Glissando()
    attach(glissando, [container])

    assert systemtools.TestManager.compare(
        container,
        r'''
        {
            c'8 \glissando
            d'8 [ \glissando
            e'8 ] \glissando
            f'8
        }
        '''
        )

    assert beam.get_timespan().stop_offset == Duration(3, 8)
    assert glissando.get_timespan().stop_offset == Duration(4, 8)
