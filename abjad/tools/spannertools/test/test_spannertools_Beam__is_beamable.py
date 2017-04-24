# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_Beam__is_beamable_01():
    r'''Eighth notes are beamable.
    Quarter notes are not beamable.
    '''

    assert Beam._is_beamable(Note(0, (1, 8)))
    assert not Beam._is_beamable(Note("c'4"))


def test_spannertools_Beam__is_beamable_02():
    r'''Containers are not beamable.
    '''

    assert not Beam._is_beamable(Staff([]))
