# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_MultipartBeam___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.MultipartBeam()
    spanner_2 = spannertools.MultipartBeam()

    assert not spanner_1 == spanner_2
