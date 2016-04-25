# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.pitchtools import Registration
from abjad.tools.pitchtools import RegistrationInventory


def test_pitchtools_RegistrationInventory___repr___01():

    inventory_1 = pitchtools.RegistrationInventory([[('[A0, C8]', -18)]])
    inventory_2 = eval(repr(inventory_1))

    assert isinstance(inventory_1, pitchtools.RegistrationInventory)
    assert isinstance(inventory_2, pitchtools.RegistrationInventory)
    assert inventory_1 == inventory_2
