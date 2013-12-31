# -*- encoding: utf-8 -*-
from experimental import *


def test_TempoInventoryEditor_run_01():
    r'''Quitting makes an empty tempo inventory.
    '''

    editor = scoremanagertools.editors.TempoInventoryEditor()
    editor._run(pending_user_input='q')
    inventory = indicatortools.TempoInventory([])
    assert editor.target == inventory


def test_TempoInventoryEditor_run_02():
    r'''Works with duration pairs.
    '''

    editor = scoremanagertools.editors.TempoInventoryEditor()
    editor._run(pending_user_input=
        'add ((1, 4), 60) '
        'add ((1, 4), 72) '
        'add ((1, 4), 84) '
        'q'
        )
    inventory = indicatortools.TempoInventory([
        Tempo(Duration(1, 4), 60), 
        Tempo(Duration(1, 4), 72), 
        Tempo(Duration(1, 4), 84),
        ])
    assert editor.target == inventory


def test_TempoInventoryEditor_run_03():
    r'''Works with durations.
    '''

    editor = scoremanagertools.editors.TempoInventoryEditor()
    editor._run(pending_user_input=
        'add (Duration(1, 4), 60) '
        'add (Duration(1, 4), 72) '
        'add (Duration(1, 4), 84) '
        'q'
        )
    inventory = indicatortools.TempoInventory([
        Tempo(Duration(1, 4), 60), 
        Tempo(Duration(1, 4), 72), 
        Tempo(Duration(1, 4), 84),
        ])
    assert editor.target == inventory
