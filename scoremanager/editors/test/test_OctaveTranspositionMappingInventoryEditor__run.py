# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_OctaveTranspositionMappingInventoryEditor__run_01():
    r'''Empty inventories.
    '''

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.OctaveTranspositionMappingInventoryEditor
    editor = editor(session=session)
    input_ = 'done'
    editor._run(pending_user_input=input_)
    assert editor.target == pitchtools.OctaveTranspositionMappingInventory()

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.OctaveTranspositionMappingInventoryEditor
    editor = editor(session=session)
    input_ = 'q'
    editor._run(pending_user_input=input_)
    assert editor.target == pitchtools.OctaveTranspositionMappingInventory()

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.OctaveTranspositionMappingInventoryEditor
    editor = editor(session=session)
    input_ = 'b'
    editor._run(pending_user_input=input_)
    assert editor.target == pitchtools.OctaveTranspositionMappingInventory()

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.OctaveTranspositionMappingInventoryEditor
    editor = editor(session=session)
    input_ = 'h'
    editor._run(pending_user_input=input_)
    assert editor.target == pitchtools.OctaveTranspositionMappingInventory()
