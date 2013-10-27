# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_notetools_NaturalHarmonic___setattr___01():
    r'''Natural harmonics are immutable.
    '''

    natural_harmonic = notetools.NaturalHarmonic("cs'8.")
    assert py.test.raises(AttributeError, "natural_harmonic.foo = 'bar'")
