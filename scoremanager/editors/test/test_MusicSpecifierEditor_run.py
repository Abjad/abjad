# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MusicSpecifierEditor_run_01():

    editor = scoremanager.editors.MusicSpecifierEditor()
    editor._run(pending_user_input='q')

    assert editor.target == scoremanager.specifiers.MusicSpecifier([])
    assert systemtools.TestManager.compare(
        format(editor.target),
        r'''
        specifiers.MusicSpecifier(
            []
            )
        ''',
        )
