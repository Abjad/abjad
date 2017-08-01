# -*- coding: utf-8 -*-
import abjad
import pytest


def test_scoretools_Note___setattr___01():
    r'''Slots constrain note attributes.
    '''

    note = abjad.Note("c'4")

    assert pytest.raises(AttributeError, "note.foo = 'bar'")
