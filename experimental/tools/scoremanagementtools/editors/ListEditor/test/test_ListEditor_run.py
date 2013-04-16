from experimental import *


def test_ListEditor_run_01():

    editor = scoremanagementtools.editors.ListEditor()
    editor.run(user_input="17 99 'foo' done q", is_autoadding=True)

    assert editor.target == [17, 99, 'foo']
