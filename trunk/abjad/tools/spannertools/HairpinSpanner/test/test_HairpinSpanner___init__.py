# -*- encoding: utf-8 -*-
from abjad import *


def test_HairpinSpanner___init___01():
    r'''Init empty hairpin spanner.
    '''

    hairpin = spannertools.HairpinSpanner()
    assert isinstance(hairpin, spannertools.HairpinSpanner)
