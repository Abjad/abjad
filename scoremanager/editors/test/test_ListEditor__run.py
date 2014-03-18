# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ListEditor__run_01():

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.ListEditor(session=session)
    input_ = "17 99 'foo' done q"
    editor._run(pending_user_input=input_, is_autoadding=True)

    assert editor.target == [17, 99, 'foo']
