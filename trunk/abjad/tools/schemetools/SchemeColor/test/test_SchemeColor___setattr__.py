from abjad import *
import py.test


def test_SchemeColor___setattr___01():
    '''Scheme colors are immutable.
    '''

    scheme_color = schemetools.SchemeColor('ForestGreen')
    assert py.test.raises(AttributeError, "scheme_color.foo = 'bar'")
