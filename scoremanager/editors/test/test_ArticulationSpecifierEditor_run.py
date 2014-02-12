# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ArticulationSpecifierEditor_run_01():

    editor = scoremanager.editors.ArticulationSpecifierEditor()
    editor._run(pending_user_input=
        'artic '
        'scoremanager.materialpackages.red_mar '
        'done'
        )
    name = 'scoremanager.materialpackages.red_marcati'
    specifier = scoremanager.specifiers.ArticulationSpecifier(
        articulation_handler_name=name
        )

    assert editor.target == specifier
