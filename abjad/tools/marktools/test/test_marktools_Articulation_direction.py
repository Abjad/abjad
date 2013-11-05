# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_Articulation_direction_01():

    note = Note("c'4")
    articulation = marktools.Articulation('staccato')
    attach(articulation, note)

    assert articulation.direction is None

    articulation.direction = '^'

    assert articulation.direction is Up
