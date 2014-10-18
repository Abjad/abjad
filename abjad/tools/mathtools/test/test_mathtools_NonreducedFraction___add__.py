# -*- encoding: utf-8 -*-
import sys
from abjad import *
from abjad.tools.mathtools import NonreducedFraction


def test_mathtools_NonreducedFraction___add___01():

    result = NonreducedFraction(1, 4) + NonreducedFraction(2, 8)
    assert result.pair == (4, 8)

    result = NonreducedFraction(2, 8) + NonreducedFraction(1, 4)
    assert result.pair == (4, 8)


def test_mathtools_NonreducedFraction___add___02():

    result = NonreducedFraction(3, 3) + 1
    assert result.pair == (6, 3)

    result = 1 + NonreducedFraction(3, 3)
    assert result.pair == (6, 3)


def test_mathtools_NonreducedFraction___add___03():

    a = mathtools.NonreducedFraction(3, 6)
    b = mathtools.NonreducedFraction(3, 12)

    result_one = systemtools.IOManager.count_function_calls(
        'a + b', locals())
    result_two = systemtools.IOManager.count_function_calls(
        'a + 10', locals())

    if sys.version_info[0] == 2:
        assert result_one == 66
        assert result_two == 35
    else:
        assert result_one == 81
        assert result_two == 40