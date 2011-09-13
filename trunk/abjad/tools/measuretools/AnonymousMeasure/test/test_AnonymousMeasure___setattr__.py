from abjad import *
import py.test


def test_AnonymousMeasure___setattr___01():
    '''Slots constraint anonymous measure attributes.
    '''

    measure = measuretools.AnonymousMeasure("c'8 d'8 e'8")

    assert py.test.raises(AttributeError, "measure.foo = 'bar'")
