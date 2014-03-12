# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_InstrumentEditor_select_instrument_01():
    r'''Quit, back, home, score & junk all work.
    '''

    session = scoremanager.core.Session()
    editor = scoremanager.editors.InstrumentEditor(session=session)
    editor._run(pending_user_input='q')
    assert editor._transcript.signature == (2,)

    session = scoremanager.core.Session()
    editor = scoremanager.editors.InstrumentEditor(session=session)
    editor._run(pending_user_input='b q')
    assert (2,)

    session = scoremanager.core.Session()
    editor = scoremanager.editors.InstrumentEditor(session=session)
    editor._run(pending_user_input='home q')
    assert (2,)

    session = scoremanager.core.Session()
    editor = scoremanager.editors.InstrumentEditor(session=session)
    editor._run(pending_user_input='score q')
    assert editor._transcript.signature == (4, (0, 2))

    session = scoremanager.core.Session()
    editor = scoremanager.editors.InstrumentEditor(session=session)
    editor._run(pending_user_input='foo q')
    assert editor._transcript.signature == (4, (0, 2))
