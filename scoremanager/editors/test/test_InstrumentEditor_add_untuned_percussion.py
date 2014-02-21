# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_InstrumentEditor_add_untuned_percussion_01():
    r'''Quit, back, score, home & junk all work.
    '''

    editor = scoremanager.editors.InstrumentEditor()
    editor._run(pending_user_input='untuned q')
    assert editor._session.transcript.signature == (4,)

    editor = scoremanager.editors.InstrumentEditor()
    editor._run(pending_user_input='untuned b')
    assert editor._session.transcript.signature == (4,)

    editor = scoremanager.editors.InstrumentEditor()
    editor._run(pending_user_input='untuned sco q')
    assert editor._session.transcript.signature == (6, (2, 4))

    editor = scoremanager.editors.InstrumentEditor()
    editor._run(pending_user_input='untuned h')
    assert editor._session.transcript.signature == (4,)

    editor = scoremanager.editors.InstrumentEditor()
    editor._run(pending_user_input='untuned foo q')
    assert editor._session.transcript.signature == (6, (2, 4))
