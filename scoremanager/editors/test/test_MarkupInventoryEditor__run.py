# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MarkupInventoryEditor__run_01():

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.MarkupInventoryEditor(session=session)
    input_ = r'add arg \italic~{~serenamente~possibile~} done done'
    editor._run(pending_user_input=input_)

    inventory = markuptools.MarkupInventory([
        markuptools.Markup(
            '\\italic { serenamente possibile }', 
            )
        ])

    assert editor.target == inventory


def test_MarkupInventoryEditor__run_02():

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.MarkupInventoryEditor(session=session)
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