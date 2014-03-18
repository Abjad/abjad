# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_TempoInventoryEditor__run_01():
    r'''Quitting makes an empty tempo inventory.
    '''

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.TempoInventoryEditor(session=session)
    input_ = 'q'
    editor._run(pending_user_input=input_)
    inventory = indicatortools.TempoInventory([])
    assert editor.target == inventory


def test_TempoInventoryEditor__run_02():
    r'''Works with duration pairs.
    '''

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.TempoInventoryEditor(session=session)
    input_ = 'add ((1, 4), 60)'
    input_ +=  ' add ((1, 4), 72)'
    input_ += ' add ((1, 4), 84) q'
    editor._run(pending_user_input=input_)
    inventory = indicatortools.TempoInventory([
        Tempo(Duration(1, 4), 60), 
        Tempo(Duration(1, 4), 72), 
        Tempo(Duration(1, 4), 84),
        ])
    assert editor.target == inventory


def test_TempoInventoryEditor__run_03():
    r'''Works with durations.
    '''

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.TempoInventoryEditor(session=session)
    input_ = 'add (Duration(1, 4), 60)'
    input_ += ' add (Duration(1, 4), 72)'
    input_ += ' add (Duration(1, 4), 84) q'
    editor._run(pending_user_input=input_)
    inventory = indicatortools.TempoInventory([
        Tempo(Duration(1, 4), 60), 
        Tempo(Duration(1, 4), 72), 
        Tempo(Duration(1, 4), 84),
        ])
    assert editor.target == inventory
