from abjad import *
import py.test


def test_SchemeMoment___setattr___01():
    '''Scheme moments are immutable.
    '''

    scheme_moment = schemetools.SchemeMoment((1, 64))
    assert py.test.raises(AttributeError, "scheme_moment.foo = 'bar'")
