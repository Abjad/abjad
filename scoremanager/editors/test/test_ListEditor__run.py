# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ListEditor__run_01():

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.ListEditor(session=session)
    input_ = "17 99 'foo' done q"
    editor._is_autoadding = True
    editor._run(pending_user_input=input_)

    assert editor.target == [17, 99, 'foo']


def test_ListEditor__run_02():

    session = scoremanager.core.Session(is_test=True)
    target = indicatortools.ClefInventory()
    editor = scoremanager.editors.ListEditor(
        session=session,
        target=target,
        )
    input_ = 'add treble add bass done'
    editor._run(pending_user_input=input_)

    inventory = indicatortools.ClefInventory(['treble', 'bass'])
    assert editor.target == inventory


def test_ListEditor__run_03():

    session = scoremanager.core.Session(is_test=True)
    target = indicatortools.ClefInventory(['treble', 'bass'])
    editor = scoremanager.editors.ListEditor(
        session=session,
        target=target,
        )
    input_ = '2 nm alto done done'
    editor._run(pending_user_input=input_)

    new_inventory = indicatortools.ClefInventory(['treble', 'alto'])
    assert editor.target == new_inventory