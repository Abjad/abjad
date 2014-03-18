# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_InstrumentEditor_add_untuned_percussion_01():
    r'''Quit, back, score, home & junk all work.
    '''

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.InstrumentEditor(session=session)
    input_ = 'untuned q'
    editor._run(pending_user_input=input_)
    assert editor._transcript.signature == (4,)

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.InstrumentEditor(session=session)
    input_ = 'untuned b'
    editor._run(pending_user_input=input_)
    assert editor._transcript.signature == (4,)

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.InstrumentEditor(session=session)
    input_ = 'untuned sco q'
    editor._run(pending_user_input=input_)
    assert editor._transcript.signature == (6, (2, 4))

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.InstrumentEditor(session=session)
    input_ = 'untuned h'
    editor._run(pending_user_input=input_)
    assert editor._transcript.signature == (4,)

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.InstrumentEditor(session=session)
    input_ = 'untuned foo q'
    editor._run(pending_user_input=input_)
    assert editor._transcript.signature == (6, (2, 4))
