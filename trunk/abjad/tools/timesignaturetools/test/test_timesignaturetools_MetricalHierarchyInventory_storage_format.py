# -*- encoding: utf-8 -*-
from abjad import *


def test_timesignaturetools_MetricalHierarchyInventory_storage_format_01():

    inventory = timesignaturetools.MetricalHierarchyInventory([(4, 4), (3, 4)])

    assert testtools.compare(
        inventory.storage_format,
        r'''
        timesignaturetools.MetricalHierarchyInventory([
            timesignaturetools.MetricalHierarchy(
                '(4/4 (1/4 1/4 1/4 1/4))'
                ),
            timesignaturetools.MetricalHierarchy(
                '(3/4 (1/4 1/4 1/4))'
                ),
            ])
        ''',
        )
