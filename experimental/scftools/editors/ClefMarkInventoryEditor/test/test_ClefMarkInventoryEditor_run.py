from abjad.tools import contexttools
import scftools


def test_ClefMarkInventoryEditor_run_01():

    editor = scftools.editors.ClefMarkInventoryEditor()
    editor.run(user_input='add treble add bass done')

    inventory = contexttools.ClefMarkInventory(['treble', 'bass'])
    assert editor.target == inventory
