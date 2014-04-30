# -*- encoding: utf-8 -*-
import fractions
import sys
from abjad import *


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
        assert result == 12

        result = systemtools.IOManager.count_function_calls(
            'mathtools.NonreducedFraction(3, 6)', globals())
        assert result == 32
