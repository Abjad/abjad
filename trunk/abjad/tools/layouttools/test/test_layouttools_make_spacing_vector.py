from abjad import *
from abjad.tools import layouttools


def test_layouttools_make_spacing_vector_01():

    spacing_vector = layouttools.make_spacing_vector(0, 0, 12, 0)
    assert spacing_vector == schemetools.SchemeVector(
        schemetools.SchemePair('basic_distance', 0),
        schemetools.SchemePair('minimum_distance', 0),
        schemetools.SchemePair('padding', 12),
        schemetools.SchemePair('stretchability', 0))
