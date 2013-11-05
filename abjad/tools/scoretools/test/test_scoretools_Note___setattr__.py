# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_scoretools_Note___setattr___01():
    r'''Slots constrain note attributes.
    '''

    note = Note("c'4")

    assert pytest.raises(AttributeError, "note.foo = 'bar'")
