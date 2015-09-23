# -*- coding: utf-8 -*-
from abjad import *


def test_datastructuretools_Cursor___eq___01():

    server = datastructuretools.Server([0, 1, 2, 3, 4])
    cursor_1 = server.make_cursor()
    cursor_2 = server.make_cursor()

    assert cursor_1 == cursor_1
    assert cursor_1 == cursor_2
    assert cursor_2 == cursor_1
    assert cursor_2 == cursor_2


def test_datastructuretools_Cursor___eq___02():

    server = datastructuretools.Server([0, 1, 2, 3, 4])
    cursor_1 = server.make_cursor()
    cursor_2 = server.make_cursor()
    cursor_1.next()

    assert cursor_1 == cursor_1
    assert cursor_1 != cursor_2
    assert cursor_2 != cursor_1
    assert cursor_2 == cursor_2