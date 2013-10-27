# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_chordtools_Chord___setattr___01():
    r'''Slots constrain chord attributes.
    '''

    chord = Chord("<ef' cs' f''>4")

    assert py.test.raises(AttributeError, "chord.foo = 'bar'")
