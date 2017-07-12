# -*- coding: utf-8 -*-
import abjad
import pytest


def test_scoretools_Skip___setattr___01():
    r'''Slots constrain skip attributes.
    '''

    skip = abjad.Skip((1, 4))

    assert pytest.raises(AttributeError, "skip.foo = 'bar'")
