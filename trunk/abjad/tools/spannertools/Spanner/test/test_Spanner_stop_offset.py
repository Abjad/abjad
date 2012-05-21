from abjad import *


def test_Spanner_stop_offset_01():
    '''Return stop time of spanner in score.
    '''

    t = Voice("c'8 d'8 e'8 f'8")
    beam = beamtools.BeamSpanner(t[1:3])
    glissando = spannertools.GlissandoSpanner([t])

    r'''
    \new Voice {
        c'8 \glissando
        d'8 [ \glissando
        e'8 ] \glissando
        f'8
    }
    '''

    assert beam.stop_offset == Duration(3, 8)
    assert glissando.stop_offset == Duration(4, 8)
