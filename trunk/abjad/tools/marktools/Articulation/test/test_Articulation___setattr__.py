from abjad import *
import py.test


def test_Articulation___setattr___01():
    '''Slots constrain articulation attributes.
    '''

    articulation = marktools.Articulation('staccato')

    assert py.test.raises(AttributeError, "articulation.foo = 'bar'")
