# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_scoretools_Note___setattr___01():
    r'''Slots constrain note attributes.
    '''

    note = Note("c'4")

    assert pytest.raises(AttributeError, "note.foo = 'bar'")
