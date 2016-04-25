# -*- coding: utf-8 -*-
from abjad import *


def test_schemetools_make_spacing_vector_01():

    spacing_vector = schemetools.make_spacing_vector(0, 0, 12, 0)
    assert spacing_vector == schemetools.SchemeVector(
        schemetools.SchemePair('basic-distance', 0),
        schemetools.SchemePair('minimum-distance', 0),
        schemetools.SchemePair('padding', 12),
        schemetools.SchemePair('stretchability', 0))
