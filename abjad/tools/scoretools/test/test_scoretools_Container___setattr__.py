# -*- coding: utf-8 -*-
import abjad
import pytest


def test_scoretools_Container___setattr___01():
    r'''Slots constrain container attributes.
    '''

    container = abjad.Container([])

    assert pytest.raises(AttributeError, "container.foo = 'bar'")
