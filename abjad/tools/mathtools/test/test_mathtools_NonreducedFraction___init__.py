# -*- coding: utf-8 -*-
import platform
import pytest
import sys
import fractions
from abjad import *
from abjad.tools import systemtools


@pytest.mark.skipif(
    platform.python_implementation() != 'CPython',
    reason='Benchmarking is only for CPython.',
    )
def test_mathtools_NonreducedFraction___init___01():
    if sys.version_info[0] == 2:
        result = systemtools.IOManager.count_function_calls(
            'fractions.Fraction(3, 6)', globals())
        assert result == 13
        result = systemtools.IOManager.count_function_calls(
            'mathtools.NonreducedFraction(3, 6)', globals())
        assert result == 30
    else:
        result = systemtools.IOManager.count_function_calls(
            'fractions.Fraction(3, 6)', globals())
        assert result < 20
        result = systemtools.IOManager.count_function_calls(
            'mathtools.NonreducedFraction(3, 6)', globals())
        assert result < 100
