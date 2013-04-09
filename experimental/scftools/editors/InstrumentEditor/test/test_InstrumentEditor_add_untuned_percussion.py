import scftools


def test_InstrumentEditor_add_untuned_percussion_01():
    '''Quit, back, score, studio & junk all work.
    '''

    editor = scftools.editors.InstrumentEditor()
    editor.run(user_input='untuned q')
    assert editor.ts == (4,)

    editor = scftools.editors.InstrumentEditor()
    editor.run(user_input='untuned b')
    assert editor.ts == (4,)

    editor = scftools.editors.InstrumentEditor()
    editor.run(user_input='untuned sco q')
    assert editor.ts == (6, (2, 4))

    editor = scftools.editors.InstrumentEditor()
    editor.run(user_input='untuned stu')
    assert editor.ts == (4,)

    editor = scftools.editors.InstrumentEditor()
    editor.run(user_input='untuned foo q')
    assert editor.ts == (6, (2, 4))
