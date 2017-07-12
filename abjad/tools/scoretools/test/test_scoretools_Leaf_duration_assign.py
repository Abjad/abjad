# -*- coding: utf-8 -*-
import abjad
import pytest


def test_scoretools_Leaf_duration_assign_01():
    r'''Written duration can be assigned a duration.
    '''

    note = abjad.Note(1, (1, 4))
    note.written_duration = abjad.Duration(1, 8)
    assert note.written_duration == abjad.Duration(1, 8)


def test_scoretools_Leaf_duration_assign_02():
    r'''Written duration can be assigned an integer.
    '''

    note = abjad.Note(1, (1, 4))
    note.written_duration = 2
    assert note.written_duration == abjad.Duration(2, 1)


def test_scoretools_Leaf_duration_assign_03():
    r'''Written duration can be assigned an tuple.
    '''

    note = abjad.Note(1, (1, 4))
    note.written_duration = (1, 2)
    assert note.written_duration == abjad.Duration(1, 2)
