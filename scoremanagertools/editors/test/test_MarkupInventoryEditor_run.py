# -*- encoding: utf-8 -*-
from experimental import *


def test_MarkupInventoryEditor_run_01():

    editor = scoremanagertools.editors.MarkupInventoryEditor()
    editor._run(pending_user_input="add arg r'\\italic~{~serenamente~possibile~}' 3 serenamente done done")

    inventory = markuptools.MarkupInventory([
        markuptools.Markup('\\italic { serenamente possibile }', markup_name='serenamente')
        ])

    assert editor.target == inventory


def test_MarkupInventoryEditor_run_02():

    editor = scoremanagertools.editors.MarkupInventoryEditor()
    editor._run(pending_user_input="name test~inventory add arg r'\\italic~{~serenamente~possibile~}' direction up name serenamente done add arg r'\\italic~{~presto~}' name presto done done")

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
