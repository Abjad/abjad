# -*- coding: utf-8 -*-
import platform
import pytest
import sys
from abjad.tools import mathtools
from abjad.tools import systemtools


def test_mathtools_NonreducedFraction___add___01():

    one = mathtools.NonreducedFraction(1, 4)
    two = mathtools.NonreducedFraction(2, 8)
    result = one + two
    assert result.pair == (4, 8)

    one = mathtools.NonreducedFraction(2, 8)
    two = mathtools.NonreducedFraction(1, 4)
    result = one + two
    assert result.pair == (4, 8)


def test_mathtools_NonreducedFraction___add___02():

    result = mathtools.NonreducedFraction(3, 3) + 1
    assert result.pair == (6, 3)

    result = 1 + mathtools.NonreducedFraction(3, 3)
    assert result.pair == (6, 3)


@pytest.mark.skipif(
    platform.python_implementation() != 'CPython',
    reason='Benchmarking is only for CPython.',
    )
def test_mathtools_NonreducedFraction___add___03():

    a = mathtools.NonreducedFraction(3, 6)
    b = mathtools.NonreducedFraction(3, 12)

    result_one = systemtools.IOManager.count_function_calls(
        'a + b', locals())
    result_two = systemtools.IOManager.count_function_calls(
        'a + 10', locals())

    if sys.version_info[0] == 2:
        assert result_one <= 80
        assert result_two <= 80
    else:
        assert result_one <= 100
        assert result_two <= 100
