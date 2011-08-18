from abjad import *
import py.test


def test_Tuplet___setattr___01():
    '''Slots constrain tuplet attributes.
    '''

    tuplet = Tuplet(Fraction(2, 3), "c'8 d'8 e'8")

    assert py.test.raises(AttributeError, "tuplet.foo = 'bar'")
