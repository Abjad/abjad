# -*- coding: utf-8 -*-
from abjad import *


def test_topleveltools_override_01():

    note = Note("c'4")
    override(note).accidental.color = 'red'
    assert override(note).accidental.color == 'red'
