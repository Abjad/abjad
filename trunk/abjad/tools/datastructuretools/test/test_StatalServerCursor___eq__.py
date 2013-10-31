# -*- encoding: utf-8 -*-
from abjad import *


def test_StatalServerCursor___eq___01():

    statal_server = datastructuretools.StatalServer([0, 1, 2, 3, 4])
    cursor_1 = statal_server()
    cursor_2 = statal_server()

    assert cursor_1 == cursor_1
    assert cursor_1 == cursor_2
    assert cursor_2 == cursor_1
    assert cursor_2 == cursor_2


def test_StatalServerCursor___eq___02():

    statal_server = datastructuretools.StatalServer([0, 1, 2, 3, 4])
    cursor_1 = statal_server()
    cursor_2 = statal_server()
    cursor_1()

    assert cursor_1 == cursor_1
    assert cursor_1 != cursor_2
    assert cursor_2 != cursor_1
    assert cursor_2 == cursor_2
