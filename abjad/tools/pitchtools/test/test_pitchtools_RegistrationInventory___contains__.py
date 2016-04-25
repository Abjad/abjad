# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_RegistrationInventory___contains___01():
    r'''Work with mappings.
    '''

    inventory = pitchtools.RegistrationInventory([[('[A0, C8]', -18)]])
    assert pitchtools.Registration([('[A0, C8]', -18)]) in inventory


def test_pitchtools_RegistrationInventory___contains___02():
    r'''Work with mapping items.
    '''

    inventory = pitchtools.RegistrationInventory([[('[A0, C8]', -18)]])
    assert [('[A0, C8]', -18)] in inventory
