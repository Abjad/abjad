from abjad import *
import py.test


def test_SchemeVectorConstant___setattr___01():
    '''Scheme vector constants are immutable.
    '''

    scheme_vector_constant = schemetools.SchemeVectorConstant(True, True, False)
    assert py.test.raises(AttributeError, "scheme_vector_constant.foo = 'bar'")
