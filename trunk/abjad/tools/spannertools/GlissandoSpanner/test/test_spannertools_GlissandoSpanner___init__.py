# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_GlissandoSpanner___init___01():
    r'''Init empty glissando spanner.
    '''

    glissando = spannertools.GlissandoSpanner()
    assert isinstance(glissando, spannertools.GlissandoSpanner)
