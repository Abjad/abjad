from abjad import *


def test_MetricalHierarchyInventory___contains___01():

    rtm = '(6/8 ((3/8 (1/8 1/8 1/8)) (3/8 (1/8 1/8 1/8))))'

    inventory = timesignaturetools.MetricalHierarchyInventory([(4, 4), (3, 4), rtm])

    assert (4, 4) in inventory
    assert timesignaturetools.MetricalHierarchy((4, 4)) in inventory

    assert (3, 4) in inventory
    assert timesignaturetools.MetricalHierarchy((3, 4)) in inventory

    assert rtm in inventory
    assert timesignaturetools.MetricalHierarchy(rtm) in inventory
