from experimental import *


def test_InstrumentEditor_select_instrument_01():
    '''Quit, back, home, score & junk all work.
    '''

    editor = scoremanagertools.editors.InstrumentEditor()
    editor._run(pending_user_input='q')
    assert editor._session.transcript.signature == (2,)

    editor = scoremanagertools.editors.InstrumentEditor()
    editor._run(pending_user_input='b q')
    assert (2,)

    editor = scoremanagertools.editors.InstrumentEditor()
    editor._run(pending_user_input='home q')
    assert (2,)

    editor = scoremanagertools.editors.InstrumentEditor()
    editor._run(pending_user_input='score q')
    assert editor._session.transcript.signature == (4, (0, 2))

    editor = scoremanagertools.editors.InstrumentEditor()
    editor._run(pending_user_input='foo q')
    assert editor._session.transcript.signature == (4, (0, 2))
