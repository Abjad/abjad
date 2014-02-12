# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MarkupInventoryEditor_run_01():

    editor = scoremanager.editors.MarkupInventoryEditor()
    string = "add arg r'\\italic~{~serenamente~possibile~}' 3 serenamente"
    string += " done done"
    editor._run(pending_user_input=string)

    inventory = markuptools.MarkupInventory([
        markuptools.Markup(
            '\\italic { serenamente possibile }', 
            markup_name='serenamente',
            )
        ])

    assert editor.target == inventory


def test_MarkupInventoryEditor_run_02():

    editor = scoremanager.editors.MarkupInventoryEditor()
    string = "name test~inventory add"
    string += " arg r'\\italic~{~serenamente~possibile~}'"
    string += " direction up name serenamente done"
    string += " add arg r'\\italic~{~presto~}' name presto done done"
    editor._run(pending_user_input=string)

    inventory = markuptools.MarkupInventory([
        markuptools.Markup(
            '\\italic { serenamente possibile }',
            direction='^',
            markup_name='serenamente'
            ),
        markuptools.Markup(
            '\\italic { presto }',
            markup_name='presto'
            )
        ],
        custom_identifier='test inventory'
        )

    assert editor.target == inventory
