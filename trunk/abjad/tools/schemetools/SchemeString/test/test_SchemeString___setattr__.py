from abjad import *
import py.test


def test_SchemeString___setattr___01():
    '''Scheme strings are immutable.
    '''

    scheme_string = schemetools.SchemeString('grace')
    assert py.test.raises(AttributeError, "scheme_string.foo = 'bar'")
