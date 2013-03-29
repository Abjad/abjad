import scf


def test_ListEditor_run_01():

    editor = scf.editors.ListEditor()
    editor.run(user_input="17 99 'foo' done q", is_autoadding=True)

    assert editor.target == [17, 99, 'foo']
