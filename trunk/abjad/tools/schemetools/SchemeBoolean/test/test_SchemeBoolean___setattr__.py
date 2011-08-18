from abjad import *
import py.test


def test_SchemeBoolean___setattr___01():
    '''Scheme booleans are immutable.
    '''

    scheme_boolean = schemetools.SchemeBoolean(False)
    assert py.test.raises(AttributeError, "scheme_boolean.foo = 'bar'")
