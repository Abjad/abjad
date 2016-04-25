# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Container___contains___01():

    note = Note("c'4")
    voice = Voice([Note("c'4")])

    assert not note in voice
