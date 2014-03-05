# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_PitchRangeInventoryEditor__run_01():

    editor = scoremanager.editors.PitchRangeInventoryEditor()
    editor._run(pending_user_input='q')
    assert editor.target == pitchtools.PitchRangeInventory([])


def test_PitchRangeInventoryEditor__run_02():

    editor = scoremanager.editors.PitchRangeInventoryEditor()
    string = 'add [C0, C6] add [C1, C7] add [C2, C8] rm 1 mv 1 2 q'
    editor._run(pending_user_input=string)
    assert editor.target == pitchtools.PitchRangeInventory([
        pitchtools.PitchRange('[C2, C8]'), 
        pitchtools.PitchRange('[C1, C7]'),
        ])
