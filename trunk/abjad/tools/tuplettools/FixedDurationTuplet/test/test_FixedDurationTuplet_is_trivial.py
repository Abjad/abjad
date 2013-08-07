# -*- encoding: utf-8 -*-
from abjad import *


def test_FixedDurationTuplet_is_trivial_01():
    r'''True when tuplet ratio equals one.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    assert not tuplet.is_trivial


def test_FixedDurationTuplet_is_trivial_02():
    r'''True when tuplet ratio equals one.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8")
    assert tuplet.is_trivial
