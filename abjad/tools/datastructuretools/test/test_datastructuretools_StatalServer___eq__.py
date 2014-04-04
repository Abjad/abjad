# -*- encoding: utf-8 -*-
from abjad import *


def test_datastructuretools_StatalServer___eq___01():

    statal_server_1 = datastructuretools.StatalServer([0, 1, 2, 3, 4])
    statal_server_2 = datastructuretools.StatalServer([0, 1, 2, 3, 4])
    statal_server_3 = datastructuretools.StatalServer([0, 1, 2, 3])

    assert     statal_server_1 == statal_server_1
    assert     statal_server_1 == statal_server_2
    assert not statal_server_1 == statal_server_3
    assert     statal_server_2 == statal_server_1
    assert     statal_server_2 == statal_server_2
    assert not statal_server_2 == statal_server_3
    assert not statal_server_3 == statal_server_1
    assert not statal_server_3 == statal_server_2
    assert     statal_server_3 == statal_server_3