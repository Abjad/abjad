from abjad import *
import py.test


def test_SchemeVariable___setattr___01():
    '''Scheme strings are immutable.
    '''

    scheme_string = schemetools.SchemeVariable('DOWN')
    assert py.test.raises(AttributeError, "scheme_string.foo = 'bar'")
