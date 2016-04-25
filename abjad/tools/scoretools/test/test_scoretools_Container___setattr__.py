# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_scoretools_Container___setattr___01():
    r'''Slots constrain container attributes.
    '''

    container = Container([])

    assert pytest.raises(AttributeError, "container.foo = 'bar'")
