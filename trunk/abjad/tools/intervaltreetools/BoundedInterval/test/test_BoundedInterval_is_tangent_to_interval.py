from abjad.tools.intervaltreetools import *
import py.test


def test_BoundedInterval_is_tangent_to_interval_01():
    a = BoundedInterval(-2, 2)
    b = BoundedInterval(-7, -3)
    assert not a.is_tangent_to_interval(b)
    assert not b.is_tangent_to_interval(a)

def test_BoundedInterval_is_tangent_to_interval_02():
    a = BoundedInterval(-2, 2)
    b = BoundedInterval(-6, -2)
    assert a.is_tangent_to_interval(b)
    assert b.is_tangent_to_interval(a)

def test_BoundedInterval_is_tangent_to_interval_03():
    a = BoundedInterval(-2, 2)
    b = BoundedInterval(-4, 0)
    assert not a.is_tangent_to_interval(b)
    assert not b.is_tangent_to_interval(a)

def test_BoundedInterval_is_tangent_to_interval_04():
    a = BoundedInterval(-2, 2)
    b = BoundedInterval(-2, 0)
    assert not a.is_tangent_to_interval(b)
    assert not b.is_tangent_to_interval(a)

def test_BoundedInterval_is_tangent_to_interval_05():
    a = BoundedInterval(-2, 2)
    b = BoundedInterval(-2, 2)
    assert not a.is_tangent_to_interval(b)
    assert not b.is_tangent_to_interval(a)

def test_BoundedInterval_is_tangent_to_interval_06():
    a = BoundedInterval(-2, 2)
    b = BoundedInterval(-1, 1)
    assert not a.is_tangent_to_interval(b)
    assert not b.is_tangent_to_interval(a)

def test_BoundedInterval_is_tangent_to_interval_07():
    a = BoundedInterval(-2, 2)
    b = BoundedInterval(0, 2)
    assert not a.is_tangent_to_interval(b)
    assert not b.is_tangent_to_interval(a)

def test_BoundedInterval_is_tangent_to_interval_08():
    a = BoundedInterval(-2, 2)
    b = BoundedInterval(0, 4)
    assert not a.is_tangent_to_interval(b)
    assert not b.is_tangent_to_interval(a)

def test_BoundedInterval_is_tangent_to_interval_09():
    a = BoundedInterval(-2, 2)
    b = BoundedInterval(2, 6)
    assert a.is_tangent_to_interval(b)
    assert b.is_tangent_to_interval(a)

def test_BoundedInterval_is_tangent_to_interval_10():
    a = BoundedInterval(-2, 2)
    b = BoundedInterval(3, 7)
    assert not a.is_tangent_to_interval(b)
    assert not b.is_tangent_to_interval(a)
