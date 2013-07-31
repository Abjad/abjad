# -*- encoding: utf-8 -*-
from abjad import *


def test_SequentialSelection_get_parent_and_stop_start_indices_01():

    t = Staff("c'8 d'8 e'8 f'8")
    parent, start, stop = t[2:]._get_parent_and_start_stop_indices()
    assert parent is t
    assert start == 2
    assert stop == 3


def test_SequentialSelection_get_parent_and_stop_start_indices_02():

    t = Staff("c'8 d'8 e'8 f'8")
    parent, start, stop = t[:2]._get_parent_and_start_stop_indices()
    assert parent is t
    assert start == 0
    assert stop == 1


def test_SequentialSelection_get_parent_and_stop_start_indices_03():

    selection = selectiontools.SequentialSelection()
    parent, start, stop = selection._get_parent_and_start_stop_indices()
    assert parent is None
    assert start is None
    assert stop is None
