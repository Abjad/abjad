from abjad import *


def test_schemetools_SchemePair__storage_format_01():

    pair = schemetools.SchemePair(-1, 1)

    assert pair._storage_format == 'schemetools.SchemePair(-1, 1)'
