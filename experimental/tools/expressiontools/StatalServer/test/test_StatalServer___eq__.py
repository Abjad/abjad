from experimental import *


def test_StatalServer___eq___01():

    statal_server_1 = expressiontools.StatalServer([0, 1, 2, 3, 4])
    statal_server_2 = expressiontools.StatalServer([0, 1, 2, 3, 4])
    statal_server_3 = expressiontools.StatalServer([0, 1, 2, 3])

    assert     statal_server_1 == statal_server_1
    assert     statal_server_1 == statal_server_2
    assert not statal_server_1 == statal_server_3
    assert     statal_server_2 == statal_server_1
    assert     statal_server_2 == statal_server_2
    assert not statal_server_2 == statal_server_3
    assert not statal_server_3 == statal_server_1
    assert not statal_server_3 == statal_server_2
    assert     statal_server_3 == statal_server_3
