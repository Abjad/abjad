# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MarkupInventoryEditor_run_01():

    editor = scoremanager.editors.MarkupInventoryEditor()
    string = "add arg r'\\italic~{~serenamente~possibile~}' done done"
    editor._run(pending_user_input=string)

    inventory = markuptools.MarkupInventory([
        markuptools.Markup(
            '\\italic { serenamente possibile }', 
            )
        ])

    assert editor.target == inventory


def test_MarkupInventoryEditor_run_02():

    editor = scoremanager.editors.MarkupInventoryEditor()
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
