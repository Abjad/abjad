from abjad.tools import mathtools
from abjad.tools import mathtools
import py.test


def test_mathtools_factors_01():
    assert py.test.raises(TypeError, 'mathtools.factors(7.5)')
    assert py.test.raises(TypeError, 'mathtools.factors(0)')


def test_mathtools_factors_02():
    t = mathtools.factors(2)
    assert t == [1, 2]


def test_mathtools_factors_03():
    t = mathtools.factors(3)
    assert t == [1, 3]


def test_mathtools_factors_04():
    t = mathtools.factors(4)
    assert t == [1, 2, 2]


def test_mathtools_factors_05():
    t = mathtools.factors(6)
    assert t == [1, 2, 3]


def test_mathtools_factors_06():
    t = mathtools.factors(12)
    assert t == [1, 2, 2, 3]
