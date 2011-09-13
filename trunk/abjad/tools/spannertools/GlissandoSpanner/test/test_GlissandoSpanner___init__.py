from abjad import *


def test_GlissandoSpanner___init___01():
    '''Init empty glissando spanner.
    '''

    glissando = spannertools.GlissandoSpanner()
    assert isinstance(glissando, spannertools.GlissandoSpanner)
