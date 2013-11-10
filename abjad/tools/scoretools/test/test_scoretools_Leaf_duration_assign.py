# -*- encoding: utf-8 -*-
import pytest
from abjad import *


def test_scoretools_Leaf_duration_assign_01():
    r'''Written duration can be assigned a duration.
    '''
    note = Note(1, (1, 4))
    note.written_duration = Duration(1, 8)
    assert note.written_duration == Duration(1, 8)


def test_scoretools_Leaf_duration_assign_02():
    r'''Written duration can be assigned an integer.
    '''
    note = Note(1, (1, 4))
    note.written_duration = 2
    assert note.written_duration == Duration(2, 1)


def test_scoretools_Leaf_duration_assign_03():
    r'''Written duration can be assigned an tuple.
    '''
    note = Note(1, (1, 4))
    note.written_duration = (1, 2)
    assert note.written_duration == Duration(1, 2)


def test_scoretools_Leaf_duration_assign_04():
    r'''Multiplier duration can be assigned a duration.
    '''
    note = Note(1, (1, 4))
    note.lilypond_duration_multiplier = Duration(1, 8)
    assert note.lilypond_duration_multiplier == Multiplier(1, 8)


def test_scoretools_Leaf_duration_assign_05():
    r'''Multiplier duration can be assigned an integer.
    '''
    note = Note(1, (1, 4))
    note.lilypond_duration_multiplier = 2
    assert note.lilypond_duration_multiplier == Multiplier(2, 1)
