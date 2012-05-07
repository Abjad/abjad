from abjad import *


def test_ComplexGlissandoSpanner___init___01():
    '''Init empty glissando spanner.
    '''

    glissando = spannertools.ComplexGlissandoSpanner()
    assert isinstance(glissando, spannertools.ComplexGlissandoSpanner)
