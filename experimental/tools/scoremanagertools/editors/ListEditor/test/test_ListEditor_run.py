from experimental import *


def test_ListEditor_run_01():

    editor = scoremanagertools.editors.ListEditor()
    editor._run(pending_user_input="17 99 'foo' done q", is_autoadding=True)

    assert editor.target == [17, 99, 'foo']
