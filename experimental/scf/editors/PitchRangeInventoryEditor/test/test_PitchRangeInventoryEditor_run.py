from abjad import *
import scf


def test_PitchRangeInventoryEditor_run_01():

    editor = scf.editors.PitchRangeInventoryEditor()
    editor.run(user_input='q')
    assert editor.target == pitchtools.PitchRangeInventory([])


def test_PitchRangeInventoryEditor_run_02():

    editor = scf.editors.PitchRangeInventoryEditor()
    editor.run(user_input='add [C0, C6] add [C1, C7] add [C2, C8] rm 1 move 1 2 q')
    assert editor.target == pitchtools.PitchRangeInventory([
        pitchtools.PitchRange('[C2, C8]'), pitchtools.PitchRange('[C1, C7]')])
