# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_ComplexGlissandoSpanner___init___01():
    r'''Init empty glissando spanner.
    '''

    glissando = spannertools.ComplexGlissandoSpanner()
    assert isinstance(glissando, spannertools.ComplexGlissandoSpanner)
