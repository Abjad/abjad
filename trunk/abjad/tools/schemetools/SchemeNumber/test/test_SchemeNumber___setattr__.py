from abjad import *
import py.test


def test_SchemeNumber___setattr___01():
    '''Scheme numbers are immutable.
    '''

    scheme_number = schemetools.SchemeNumber(-1)
    assert py.test.raises(AttributeError, "scheme_number.foo = 'bar'")
