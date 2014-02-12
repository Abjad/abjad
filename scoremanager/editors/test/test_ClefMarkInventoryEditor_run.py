# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ClefMarkInventoryEditor_run_01():

    editor = scoremanager.editors.ClefInventoryEditor()
    editor._run(pending_user_input='add treble add bass done')

    inventory = indicatortools.ClefInventory(['treble', 'bass'])
    assert editor.target == inventory
