from abjad import *
import py.test


def test_MultiMeasureRest___setattr___01():

    rest = resttools.MultiMeasureRest((1, 4))

    assert py.test.raises(AttributeError, "rest.foo = 'bar'")
