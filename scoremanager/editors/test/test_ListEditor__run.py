# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ListEditor__run_01():
    r'''Edits buil-in list.
    '''

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.ListEditor(session=session)
    input_ = "17 99 'foo' done q"
    editor._is_autoadding = True
    editor._run(pending_user_input=input_)

    assert editor.target == [17, 99, 'foo']


def test_ListEditor__run_02():
    r'''Edits empty clef inventory.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = indicatortools.ClefInventory()
    editor = scoremanager.editors.ListEditor(
        session=session,
        target=target,
        )
    input_ = 'add nm treble done add nm bass done done'
    editor._run(pending_user_input=input_)

    inventory = indicatortools.ClefInventory(['treble', 'bass'])
    assert editor.target == inventory


def test_ListEditor__run_03():
    r'''Edits nonempty clef inventory.
    '''

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


def test_ListEditor__run_04():
    r'''Edits empty markup inventory.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = markuptools.MarkupInventory()
    editor = scoremanager.editors.ListEditor(
        session=session,
        target=target,
        )
    input_ = r'add arg \italic~{~serenamente~possibile~} done done'
    editor._run(pending_user_input=input_)

    inventory = markuptools.MarkupInventory([
        markuptools.Markup(
            '\\italic { serenamente possibile }', 
            )
        ])

    assert editor.target == inventory


def test_ListEditor__run_05():
    r'''Edits nonempty markup inventory.
    '''

    session = scoremanager.core.Session(is_test=True)
    target = markuptools.MarkupInventory()
    editor = scoremanager.editors.ListEditor(
        session=session,
        target=target,
        )
    input_ = 'add'
    input_ += r' arg \italic~{~serenamente~possibile~}'
    input_ += ' direction up done'
    input_ += r' add arg \italic~{~presto~} done done'
    editor._run(pending_user_input=input_)

    inventory = markuptools.MarkupInventory([
        markuptools.Markup(
            '\\italic { serenamente possibile }',
            direction='^',
            ),
        markuptools.Markup(
            '\\italic { presto }',
            )
        ],
        )

    assert editor.target == inventory