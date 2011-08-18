from abjad import *
import py.test


def test_SchemeAssociativeList___setattr___01():
    '''Scheme associative lists are immutable.
    '''

    scheme_alist = schemetools.SchemeAssociativeList(('space', 2), ('padding', 0.5))
    assert py.test.raises(AttributeError, "scheme_alist.foo = 'bar'")
