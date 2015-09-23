# -*- coding: utf-8 -*-
from abjad import *


def test_datastructuretools_Server___eq___01():

    server_1 = datastructuretools.Server([0, 1, 2, 3, 4])
    server_2 = datastructuretools.Server([0, 1, 2, 3, 4])
    server_3 = datastructuretools.Server([0, 1, 2, 3])

    assert     server_1 == server_1
    assert     server_1 == server_2
    assert not server_1 == server_3
    assert     server_2 == server_1
    assert     server_2 == server_2
    assert not server_2 == server_3
    assert not server_3 == server_1
    assert not server_3 == server_2
    assert     server_3 == server_3