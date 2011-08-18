from abjad import *
import py.test


def test_SchemeFunction___setattr___01():
    '''Scheme functions are immutable.
    '''

    scheme_function = schemetools.SchemeFunction('magstep', -3)
    assert py.test.raises(AttributeError, "scheme_function.foo = 'bar'")
