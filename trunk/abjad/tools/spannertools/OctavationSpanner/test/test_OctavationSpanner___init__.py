# -*- encoding: utf-8 -*-
from abjad import *


def test_OctavationSpanner___init___01():
    r'''Init empty octavation spanner.
    '''

    octavation = spannertools.OctavationSpanner()
    assert isinstance(octavation, spannertools.OctavationSpanner)
