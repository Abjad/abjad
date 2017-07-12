# -*- coding: utf-8 -*-
import abjad
import pytest


def test_scoretools_MultimeasureRest___setattr___01():

    rest = abjad.MultimeasureRest((1, 4))

    assert pytest.raises(AttributeError, "rest.foo = 'bar'")
