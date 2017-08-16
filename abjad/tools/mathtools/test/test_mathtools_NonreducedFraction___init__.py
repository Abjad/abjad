import abjad
import platform
import pytest


@pytest.mark.skipif(
    platform.python_implementation() != 'CPython',
    reason='Benchmarking is only for CPython.',
    )
def test_mathtools_NonreducedFraction___init___01():
    result = abjad.IOManager.count_function_calls(
        'abjad.Fraction(3, 6)', globals())
    assert result < 20
    result = abjad.IOManager.count_function_calls(
        'abjad.NonreducedFraction(3, 6)', globals())
    assert result < 100
