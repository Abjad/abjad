from abjad import *
import py.test


def test_SchemeVector___setattr___01():
    '''Scheme vectors are immutable.
    '''

    scheme_vector = schemetools.SchemeVector(True, True, False)
    assert py.test.raises(AttributeError, "scheme_vector.foo = 'bar'")
