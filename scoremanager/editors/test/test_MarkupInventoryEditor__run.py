# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MarkupInventoryEditor__run_01():

    session = scoremanager.core.Session()
    editor = scoremanager.editors.MarkupInventoryEditor(session=session)
    string = "add arg r'\\italic~{~serenamente~possibile~}' done done"
    editor._run(pending_user_input=string)

    inventory = markuptools.MarkupInventory([
        markuptools.Markup(
            '\\italic { serenamente possibile }', 
            )
        ])

    assert editor.target == inventory


def test_MarkupInventoryEditor__run_02():

    session = scoremanager.core.Session()
    editor = scoremanager.editors.MarkupInventoryEditor(session=session)
    string = "add"
    string += " arg r'\\italic~{~serenamente~possibile~}'"
    string += " direction up done"
    string += " add arg r'\\italic~{~presto~}' done done"
    editor._run(pending_user_input=string)

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
