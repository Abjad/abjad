# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_scoretools_Tuplet___setattr___01():
    r'''Slots constrain tuplet attributes.
    '''

    tuplet = Tuplet(Multiplier(2, 3), "c'8 d'8 e'8")

    assert pytest.raises(AttributeError, "tuplet.foo = 'bar'")
