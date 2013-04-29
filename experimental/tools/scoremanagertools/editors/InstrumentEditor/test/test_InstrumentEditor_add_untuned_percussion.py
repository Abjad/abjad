from experimental import *


def test_InstrumentEditor_add_untuned_percussion_01():
    '''Quit, back, score, home & junk all work.
    '''

    editor = scoremanagertools.editors.InstrumentEditor()
    editor.run(user_input='untuned q')
    assert editor.session.transcript_signature == (4,)

    editor = scoremanagertools.editors.InstrumentEditor()
    editor.run(user_input='untuned b')
    assert editor.session.transcript_signature == (4,)

    editor = scoremanagertools.editors.InstrumentEditor()
    editor.run(user_input='untuned sco q')
    assert editor.session.transcript_signature == (6, (2, 4))

    editor = scoremanagertools.editors.InstrumentEditor()
    editor.run(user_input='untuned home')
    assert editor.session.transcript_signature == (4,)

    editor = scoremanagertools.editors.InstrumentEditor()
    editor.run(user_input='untuned foo q')
    assert editor.session.transcript_signature == (6, (2, 4))
