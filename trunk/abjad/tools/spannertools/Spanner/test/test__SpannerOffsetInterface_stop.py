from abjad import *


def test__SpannerOffsetInterface_stop_01():
    '''Return stop time of spanner in score.'''

    t = Voice("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner(t[1:3])
    glissando = spannertools.GlissandoSpanner([t])

    r'''
    \new Voice {
        c'8 \glissando
        d'8 [ \glissando
        e'8 ] \glissando
        f'8
    }
    '''

    assert beam._offset.stop == Duration(3, 8)
    assert glissando._offset.stop == Duration(4, 8)
