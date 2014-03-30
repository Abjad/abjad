# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Editor__edit_01():

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.Editor(session=session)
    editor._session._pending_user_input = 'nm alto done'
    editor._edit(Clef)

    assert editor.target == Clef('alto')