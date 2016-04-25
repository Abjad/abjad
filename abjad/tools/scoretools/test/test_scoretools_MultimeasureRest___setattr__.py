# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_scoretools_MultimeasureRest___setattr___01():

    rest = scoretools.MultimeasureRest((1, 4))

    assert pytest.raises(AttributeError, "rest.foo = 'bar'")
