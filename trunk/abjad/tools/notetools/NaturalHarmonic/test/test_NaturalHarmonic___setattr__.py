from abjad import *
import py.test


def test_NaturalHarmonic___setattr___01():
    '''Natural harmonics are immutable.
    '''

    natural_harmonic = notetools.NaturalHarmonic("cs'8.")
    assert py.test.raises(AttributeError, "natural_harmonic.foo = 'bar'")
