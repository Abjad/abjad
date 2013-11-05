# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_scoretools_Container___setattr___01():
    r'''Slots constrain container attributes.
    '''

    container = Container([])

    assert pytest.raises(AttributeError, "container.foo = 'bar'")
