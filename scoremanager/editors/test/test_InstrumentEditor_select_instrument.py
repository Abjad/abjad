# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_InstrumentEditor_select_instrument_01():
    r'''Quit, back, home, score & junk all work.
    '''

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.InstrumentEditor(session=session)
    input_ = 'q'
    editor._run(pending_user_input=input_)
    assert editor._transcript.signature == (2,)

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.InstrumentEditor(session=session)
    input_ = 'b q'
    editor._run(pending_user_input=input_)
    assert (2,)

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.InstrumentEditor(session=session)
    input_ = 'h q'
    editor._run(pending_user_input=input_)
    assert (2,)

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.InstrumentEditor(session=session)
    input_ = 's q'
    editor._run(pending_user_input=input_)
    assert editor._transcript.signature == (4, (0, 2))

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.InstrumentEditor(session=session)
    input_ = 'foo q'
    editor._run(pending_user_input=input_)
    assert editor._transcript.signature == (4, (0, 2))
