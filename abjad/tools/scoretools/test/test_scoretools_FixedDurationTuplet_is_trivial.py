# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_FixedDurationTuplet_is_trivial_01():
    r'''Is true when tuplet ratio equals one.
    '''

    tuplet = scoretools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8")
    assert tuplet.is_trivial


def test_scoretools_FixedDurationTuplet_is_trivial_02():
    r'''False when tuplet ratio does not equal one.
    '''

    tuplet = scoretools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    assert not tuplet.is_trivial
