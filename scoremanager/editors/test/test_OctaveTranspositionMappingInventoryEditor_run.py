# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_OctaveTranspositionMappingInventoryEditor_run_01():
    r'''Empty inventories.
    '''

    editor = scoremanager.editors.OctaveTranspositionMappingInventoryEditor()
    editor._run(pending_user_input='done')
    assert editor.target == pitchtools.OctaveTranspositionMappingInventory()

    editor = scoremanager.editors.OctaveTranspositionMappingInventoryEditor()
    editor._run(pending_user_input='q')
    assert editor.target == pitchtools.OctaveTranspositionMappingInventory()

    editor = scoremanager.editors.OctaveTranspositionMappingInventoryEditor()
    editor._run(pending_user_input='b')
    assert editor.target == pitchtools.OctaveTranspositionMappingInventory()

    editor = scoremanager.editors.OctaveTranspositionMappingInventoryEditor()
    editor._run(pending_user_input='home')
    assert editor.target == pitchtools.OctaveTranspositionMappingInventory()


def test_OctaveTranspositionMappingInventoryEditor_run_02():
    r'''Empty named inventory.
    '''

    editor = scoremanager.editors.OctaveTranspositionMappingInventoryEditor()
    editor._run(pending_user_input='id foo done')
    assert editor.target == \
        pitchtools.OctaveTranspositionMappingInventory(custom_identifier='foo')


def test_OctaveTranspositionMappingInventoryEditor_run_03():
    r'''Named inventory with named mapping.
    '''

    editor = scoremanager.editors.OctaveTranspositionMappingInventoryEditor()
    editor._run(pending_user_input=
        'id mapping~inventory '
        'add name piccolo~strict~first~octave '
        'add source [A0, C8] target 14 '
        'done done done '
        )

    inventory = pitchtools.OctaveTranspositionMappingInventory(
        [pitchtools.OctaveTranspositionMapping(
            [('[A0, C8]', 14)],
            custom_identifier='piccolo strict first octave')],
        custom_identifier='mapping inventory'
        )

    assert editor.target == inventory
