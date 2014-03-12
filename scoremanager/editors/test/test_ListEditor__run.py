# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ListEditor__run_01():

    session = scoremanager.core.Session()
    editor = scoremanager.editors.ListEditor(session=session)
    editor._run(pending_user_input="17 99 'foo' done q", is_autoadding=True)

    assert editor.target == [17, 99, 'foo']
