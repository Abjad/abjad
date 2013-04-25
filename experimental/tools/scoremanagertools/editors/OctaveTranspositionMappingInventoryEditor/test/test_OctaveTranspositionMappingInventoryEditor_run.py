from abjad.tools import pitchtools
from experimental import *


def test_OctaveTranspositionMappingInventoryEditor_run_01():
    '''Empty inventories.
    '''

    editor = scoremanagertools.editors.OctaveTranspositionMappingInventoryEditor()
    editor.run(user_input='done')
    assert editor.target == pitchtools.OctaveTranspositionMappingInventory()

    editor = scoremanagertools.editors.OctaveTranspositionMappingInventoryEditor()
    editor.run(user_input='q')
    assert editor.target == pitchtools.OctaveTranspositionMappingInventory()

    editor = scoremanagertools.editors.OctaveTranspositionMappingInventoryEditor()
    editor.run(user_input='b')
    assert editor.target == pitchtools.OctaveTranspositionMappingInventory()

    editor = scoremanagertools.editors.OctaveTranspositionMappingInventoryEditor()
    editor.run(user_input='home')
    assert editor.target == pitchtools.OctaveTranspositionMappingInventory()


def test_OctaveTranspositionMappingInventoryEditor_run_02():
    '''Empty named inventory.
    '''

    editor = scoremanagertools.editors.OctaveTranspositionMappingInventoryEditor()
    editor.run(user_input='name foo done')
    assert editor.target == pitchtools.OctaveTranspositionMappingInventory(name='foo')


def test_OctaveTranspositionMappingInventoryEditor_run_03():
    '''Named inventory with named mapping.
    '''

    editor = scoremanagertools.editors.OctaveTranspositionMappingInventoryEditor()
    editor.run(user_input=
        'name mapping~inventory '
        'add name piccolo~strict~first~octave '
        'add source [A0, C8] target 14 '
        'done done done '
        )

    inventory = pitchtools.OctaveTranspositionMappingInventory(
        [pitchtools.OctaveTranspositionMapping(
            [('[A0, C8]', 14)],
            name='piccolo strict first octave')],
        name='mapping inventory'
        )

    assert editor.target == inventory
