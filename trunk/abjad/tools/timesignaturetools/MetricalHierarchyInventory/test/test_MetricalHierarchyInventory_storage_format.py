from abjad import *


def test_MetricalHierarchyInventory_storage_format_01():

    inventory = timesignaturetools.MetricalHierarchyInventory([(4, 4), (3, 4)])

    r'''
    timesignaturetools.MetricalHierarchyInventory([
        timesignaturetools.MetricalHierarchy(
            '(4/4 (1/4 1/4 1/4 1/4))'
            ),
        timesignaturetools.MetricalHierarchy(
            '(3/4 (1/4 1/4 1/4))'
            )
        ])
    '''

    assert inventory.storage_format == "timesignaturetools.MetricalHierarchyInventory([\n\ttimesignaturetools.MetricalHierarchy(\n\t\t'(4/4 (1/4 1/4 1/4 1/4))'\n\t\t),\n\ttimesignaturetools.MetricalHierarchy(\n\t\t'(3/4 (1/4 1/4 1/4))'\n\t\t)\n\t])"
