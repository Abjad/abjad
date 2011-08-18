from abjad import Fraction
from abjad.tools.intervaltreetools import *
import py.test


def test_intervaltreetools_calculate_depth_density_of_intervals_in_interval_01():
    a = BoundedInterval(0, 10)
    b = BoundedInterval(5, 15)
    c = BoundedInterval(20, 25)
    assert calculate_depth_density_of_intervals_in_interval([a, b, c],
        BoundedInterval(-10, -5)) == 0


def test_intervaltreetools_calculate_depth_density_of_intervals_in_interval_02():
    a = BoundedInterval(0, 10)
    b = BoundedInterval(5, 15)
    c = BoundedInterval(20, 25)
    assert calculate_depth_density_of_intervals_in_interval([a, b, c],
        BoundedInterval(30, 40)) == 0


def test_intervaltreetools_calculate_depth_density_of_intervals_in_interval_03():
    a = BoundedInterval(0, 10)
    b = BoundedInterval(5, 15)
    c = BoundedInterval(20, 25)
    assert calculate_depth_density_of_intervals_in_interval([a, b, c],
        BoundedInterval(0, 5)) == 1


def test_intervaltreetools_calculate_depth_density_of_intervals_in_interval_04():
    a = BoundedInterval(0, 10)
    b = BoundedInterval(5, 15)
    c = BoundedInterval(20, 25)
    assert calculate_depth_density_of_intervals_in_interval([a, b, c],
        BoundedInterval(0, 10)) == Fraction(3, 2)


def test_intervaltreetools_calculate_depth_density_of_intervals_in_interval_05():
    a = BoundedInterval(0, 10)
    b = BoundedInterval(5, 15)
    c = BoundedInterval(20, 25)
    assert calculate_depth_density_of_intervals_in_interval([a, b, c],
        BoundedInterval(0, 15)) == Fraction(4, 3)


def test_intervaltreetools_calculate_depth_density_of_intervals_in_interval_06():
    a = BoundedInterval(0, 10)
    b = BoundedInterval(5, 15)
    c = BoundedInterval(20, 25)
    assert calculate_depth_density_of_intervals_in_interval([a, b, c],
        BoundedInterval(0, 20)) == 1


def test_intervaltreetools_calculate_depth_density_of_intervals_in_interval_07():
    a = BoundedInterval(0, 10)
    b = BoundedInterval(5, 15)
    c = BoundedInterval(20, 25)
    assert calculate_depth_density_of_intervals_in_interval([a, b, c],
        BoundedInterval(0, 25)) == 1
