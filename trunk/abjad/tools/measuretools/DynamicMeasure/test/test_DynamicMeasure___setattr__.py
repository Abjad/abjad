from abjad import *
import py.test


def test_DynamicMeasure___setattr___01():
    '''Slots constraint dynamic measure attributes.
    '''

    measure = measuretools.DynamicMeasure("c'8 d'8 e'8")

    assert py.test.raises(AttributeError, "measure.foo = 'bar'")
