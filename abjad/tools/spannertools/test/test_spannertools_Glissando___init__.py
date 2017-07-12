# -*- coding: utf-8 -*-
import abjad


def test_spannertools_Glissando___init___01():
    r'''Initialize empty glissando spanner.
    '''

    glissando = abjad.Glissando()
    assert isinstance(glissando, abjad.Glissando)
