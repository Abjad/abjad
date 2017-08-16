import abjad
import platform
import pytest


def test_mathtools_NonreducedFraction___add___01():

    one = abjad.NonreducedFraction(1, 4)
    two = abjad.NonreducedFraction(2, 8)
    result = one + two
    assert result.pair == (4, 8)

    one = abjad.NonreducedFraction(2, 8)
    two = abjad.NonreducedFraction(1, 4)
    result = one + two
    assert result.pair == (4, 8)


def test_mathtools_NonreducedFraction___add___02():

    result = abjad.NonreducedFraction(3, 3) + 1
    assert result.pair == (6, 3)

    result = 1 + abjad.NonreducedFraction(3, 3)
    assert result.pair == (6, 3)


@pytest.mark.skipif(
    platform.python_implementation() != 'CPython',
    reason='Benchmarking is only for CPython.',
    )
def test_mathtools_NonreducedFraction___add___03():

    a = abjad.NonreducedFraction(3, 6)
    b = abjad.NonreducedFraction(3, 12)

    result_one = abjad.IOManager.count_function_calls(
        'a + b', locals())
    result_two = abjad.IOManager.count_function_calls(
        'a + 10', locals())

    assert result_one <= 110
    assert result_two <= 110
