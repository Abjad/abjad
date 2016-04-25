# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_scoretools_Voice___setattr___01():
    r'''Slots constrain voice attributes.
    '''

    voice = Voice([])

    assert pytest.raises(AttributeError, "voice.foo = 'bar'")
