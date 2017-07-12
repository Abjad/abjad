# -*- coding: utf-8 -*-
import abjad


def test_spannertools_Spanner_start_offset_01():
    r'''Returns start time of spanner in score.
    '''

    container = abjad.Container("c'8 d'8 e'8 f'8")
    beam = abjad.Beam()
    abjad.attach(beam, container[1:3])
    glissando = abjad.Glissando()
    abjad.attach(glissando, container[:])

    assert format(container) == abjad.String.normalize(
        r'''
        {
            c'8 \glissando
            d'8 [ \glissando
            e'8 ] \glissando
            f'8
        }
        '''
        )

    assert abjad.inspect(beam).get_timespan().start_offset == abjad.Duration(1, 8)
    assert abjad.inspect(glissando).get_timespan().start_offset == abjad.Duration(0)
