# -*- coding: utf-8 -*-
from abjad import *


def test_datastructuretools_Cursor___eq___01():

    server = datastructuretools.Server([0, 1, 2, 3, 4])
    cursor_1 = datastructuretools.Cursor(source=server)
    cursor_2 = datastructuretools.Cursor(source=server)

    assert cursor_1 == cursor_1
    assert cursor_1 == cursor_2
    assert cursor_2 == cursor_1
    assert cursor_2 == cursor_2


def test_datastructuretools_Cursor___eq___02():

    server = datastructuretools.Server([0, 1, 2, 3, 4])
    cursor_1 = datastructuretools.Cursor(source=server)
    cursor_2 = datastructuretools.Cursor(source=server)
    cursor_1.next()

    assert cursor_1 == cursor_1
    assert cursor_1 != cursor_2
    assert cursor_2 != cursor_1
    assert cursor_2 == cursor_2