# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_RegistrationInventory_append_01():
    r'''Append named item.
    '''

    inventory = pitchtools.RegistrationInventory()
    assert repr(inventory) == 'RegistrationInventory([])'
