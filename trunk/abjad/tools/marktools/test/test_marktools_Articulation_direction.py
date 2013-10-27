# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_Articulation_direction_01():

    note = Note("c'4")
    a = marktools.Articulation('staccato')(note)

    assert a.direction is None

    a.direction = '^'

    assert a.direction is Up
