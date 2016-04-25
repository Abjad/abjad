# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_Glissando___init___01():
    r'''Initialize empty glissando spanner.
    '''

    glissando = spannertools.Glissando()
    assert isinstance(glissando, spannertools.Glissando)
