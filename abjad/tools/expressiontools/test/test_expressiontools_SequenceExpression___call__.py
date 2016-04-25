# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_expressiontools_SequenceExpression___call___01():

    expression = sequence()
    statement = 'expression(1, 2, 3)'

    assert pytest.raises(TypeError, statement)
