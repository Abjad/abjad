# -*- encoding: utf-8 -*-
from abjad.tools import marktools
from experimental import *


def test_ClefMarkInventoryEditor_run_01():

    editor = scoremanagertools.editors.ClefMarkInventoryEditor()
    editor._run(pending_user_input='add treble add bass done')

    inventory = marktools.ClefInventory(['treble', 'bass'])
    assert editor.target == inventory
