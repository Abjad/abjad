# -*- encoding: utf-8 -*-
import copy
from abjad import *
from scoremanager import idetools


def test_ViewInventory___deepcopy___01():
    
    inventory_1 = idetools.ViewInventory()
    inventory_2 = copy.deepcopy(inventory_1)

    assert inventory_1 == inventory_2
    assert repr(inventory_1) == repr(inventory_2)