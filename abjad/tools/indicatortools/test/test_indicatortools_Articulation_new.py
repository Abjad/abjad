# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_Articulation_new_01():
    old_articulation = Articulation('.')
    new_articulation = new(old_articulation)
    assert repr(new_articulation) == "Articulation('.')"
