# -*- encoding: utf-8 -*-
from abjad import *


def test_lilypondproxytools_LilyPondGrobProxy___setattr___01():

    note = Note("c'4")
    override(note).accidental.color = 'red'
    assert override(note).accidental.color == 'red'
