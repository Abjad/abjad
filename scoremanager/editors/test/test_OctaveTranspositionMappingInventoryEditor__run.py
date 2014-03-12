# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_OctaveTranspositionMappingInventoryEditor__run_01():
    r'''Empty inventories.
    '''

    session = scoremanager.core.Session()
    editor = scoremanager.editors.OctaveTranspositionMappingInventoryEditor
    editor = editor(session=session)
    editor._run(pending_user_input='done')
    assert editor.target == pitchtools.OctaveTranspositionMappingInventory()

    session = scoremanager.core.Session()
    editor = scoremanager.editors.OctaveTranspositionMappingInventoryEditor
    editor = editor(session=session)
    editor._run(pending_user_input='q')
    assert editor.target == pitchtools.OctaveTranspositionMappingInventory()

    session = scoremanager.core.Session()
    editor = scoremanager.editors.OctaveTranspositionMappingInventoryEditor
    editor = editor(session=session)
    editor._run(pending_user_input='b')
    assert editor.target == pitchtools.OctaveTranspositionMappingInventory()

    session = scoremanager.core.Session()
    editor = scoremanager.editors.OctaveTranspositionMappingInventoryEditor
    editor = editor(session=session)
    editor._run(pending_user_input='h')
    assert editor.target == pitchtools.OctaveTranspositionMappingInventory()
