from fractions import Fraction
from abjad.tools.timeintervaltools import *
import py.test


def test_timeintervaltools_calculate_depth_density_of_intervals_in_interval_01():
    a = TimeInterval(0, 10)
    b = TimeInterval(5, 15)
    c = TimeInterval(20, 25)
    assert calculate_depth_density_of_intervals_in_interval([a, b, c],
        TimeInterval(-10, -5)) == 0


def test_timeintervaltools_calculate_depth_density_of_intervals_in_interval_02():
    a = TimeInterval(0, 10)
    b = TimeInterval(5, 15)
    c = TimeInterval(20, 25)
    assert calculate_depth_density_of_intervals_in_interval([a, b, c],
        TimeInterval(30, 40)) == 0


def test_timeintervaltools_calculate_depth_density_of_intervals_in_interval_03():
    a = TimeInterval(0, 10)
    b = TimeInterval(5, 15)
    c = TimeInterval(20, 25)
    assert calculate_depth_density_of_intervals_in_interval([a, b, c],
        TimeInterval(0, 5)) == 1


def test_timeintervaltools_calculate_depth_density_of_intervals_in_interval_04():
    a = TimeInterval(0, 10)
    b = TimeInterval(5, 15)
    c = TimeInterval(20, 25)
    assert calculate_depth_density_of_intervals_in_interval([a, b, c],
        TimeInterval(0, 10)) == Fraction(3, 2)


def test_timeintervaltools_calculate_depth_density_of_intervals_in_interval_05():
    a = TimeInterval(0, 10)
    b = TimeInterval(5, 15)
    c = TimeInterval(20, 25)
    assert calculate_depth_density_of_intervals_in_interval([a, b, c],
        TimeInterval(0, 15)) == Fraction(4, 3)


def test_timeintervaltools_calculate_depth_density_of_intervals_in_interval_06():
    a = TimeInterval(0, 10)
    b = TimeInterval(5, 15)
    c = TimeInterval(20, 25)
    assert calculate_depth_density_of_intervals_in_interval([a, b, c],
        TimeInterval(0, 20)) == 1


def test_timeintervaltools_calculate_depth_density_of_intervals_in_interval_07():
    a = TimeInterval(0, 10)
    b = TimeInterval(5, 15)
    c = TimeInterval(20, 25)
    assert calculate_depth_density_of_intervals_in_interval([a, b, c],
        TimeInterval(0, 25)) == 1
