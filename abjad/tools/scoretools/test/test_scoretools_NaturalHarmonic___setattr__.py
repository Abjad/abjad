# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_scoretools_NaturalHarmonic___setattr___01():
    r'''Natural harmonics are immutable.
    '''

    natural_harmonic = scoretools.NaturalHarmonic("cs'8.")
    assert pytest.raises(AttributeError, "natural_harmonic.foo = 'bar'")
