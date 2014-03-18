# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ClefInventoryEditor__run_01():

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.ClefInventoryEditor(session=session)
    input_ = 'add treble add bass done'
    editor._run(pending_user_input=input_)

    inventory = indicatortools.ClefInventory(['treble', 'bass'])
    assert editor.target == inventory
