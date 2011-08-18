from abjad import *
import py.test


def test_SchemePair___setattr___01():
    '''Scehem pairs are immutable.
    '''

    scheme_pair = schemetools.SchemePair('spacing', 4)
    assert py.test.raises(AttributeError, "scheme_pair.foo = 'bar'")
