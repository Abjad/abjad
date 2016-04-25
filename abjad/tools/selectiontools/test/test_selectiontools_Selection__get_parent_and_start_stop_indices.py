# -*- coding: utf-8 -*-
from abjad import *


def test_selectiontools_Selection__get_parent_and_start_stop_indices_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    parent, start, stop = staff[2:]._get_parent_and_start_stop_indices()
    assert parent is staff
    assert start == 2
    assert stop == 3


def test_selectiontools_Selection__get_parent_and_start_stop_indices_02():

    staff = Staff("c'8 d'8 e'8 f'8")
    parent, start, stop = staff[:2]._get_parent_and_start_stop_indices()
    assert parent is staff
    assert start == 0
    assert stop == 1


def test_selectiontools_Selection__get_parent_and_start_stop_indices_03():

    selection = selectiontools.Selection()
    parent, start, stop = selection._get_parent_and_start_stop_indices()
    assert parent is None
    assert start is None
    assert stop is None
