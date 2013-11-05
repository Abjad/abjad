# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_scoretools_Note___setattr___01():
    r'''Slots constrain note attributes.
    '''

    note = Note("c'4")

    assert py.test.raises(AttributeError, "note.foo = 'bar'")
