# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_scoretools_Voice___setattr___01():
    r'''Slots constrain voice attributes.
    '''

    voice = Voice([])

    assert pytest.raises(AttributeError, "voice.foo = 'bar'")
