# -*- coding: utf-8 -*-
from abjad import *


def test_selectiontools_Selection__get_offset_lists_01():

    staff = Staff("c'4 d'4 e'4 f'4")
    selection = staff[:2]
    start_offsets, stop_offsets = selection._get_offset_lists()

    assert start_offsets == [Offset(0, 1), Offset(1, 4)]
    assert stop_offsets == [Offset(1, 4), Offset(1, 2)]
