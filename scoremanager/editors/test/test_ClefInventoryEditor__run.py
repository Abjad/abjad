# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
session = scoremanager.core.Session(is_test=True)


def test_ClefInventoryEditor__run_01():

    editor = scoremanager.editors.ClefInventoryEditor(session=session)
    input_ = 'add treble add bass done'
    editor._run(pending_user_input=input_)

    inventory = indicatortools.ClefInventory(['treble', 'bass'])
    assert editor.target == inventory


def test_ClefInventoryEditor__run_02():

    inventory = indicatortools.ClefInventory(['treble', 'bass'])
    editor = scoremanager.editors.ClefInventoryEditor(
        session=session,
        target=inventory,
        )
    input_ = '2 nm alto done done'
    editor._run(pending_user_input=input_)

    new_inventory = indicatortools.ClefInventory(['treble', 'alto'])
    assert editor.target == new_inventory