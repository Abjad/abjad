from abjad.tools import contexttools
import scf


def test_ClefMarkInventoryEditor_run_01():

    editor = scf.editors.ClefMarkInventoryEditor()
    editor.run(user_input='add treble add bass done')

    inventory = contexttools.ClefMarkInventory(['treble', 'bass'])
    assert editor.target == inventory
