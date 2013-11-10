# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_tmp_MultimeasureRest___setattr___01():

    rest = scoretools.MultimeasureRest((1, 4))

    assert pytest.raises(AttributeError, "rest.foo = 'bar'")
