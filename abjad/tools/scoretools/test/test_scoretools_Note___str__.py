# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Note___str___01():

    note = Note("c'4")

    assert str(note) == "c'4"
