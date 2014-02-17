# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_InstrumentEditor_add_untuned_percussion_01():
    r'''Quit, back, score, home & junk all work.
    '''

    editor = scoremanager.editors.InstrumentEditor()
    editor._run(pending_user_input='untuned q')
    assert editor.session.io_transcript.signature == (4,)

    editor = scoremanager.editors.InstrumentEditor()
    editor._run(pending_user_input='untuned b')
    assert editor.session.io_transcript.signature == (4,)

    editor = scoremanager.editors.InstrumentEditor()
    editor._run(pending_user_input='untuned sco q')
    assert editor.session.io_transcript.signature == (6, (2, 4))

    editor = scoremanager.editors.InstrumentEditor()
    editor._run(pending_user_input='untuned home')
    assert editor.session.io_transcript.signature == (4,)

    editor = scoremanager.editors.InstrumentEditor()
    editor._run(pending_user_input='untuned foo q')
    assert editor.session.io_transcript.signature == (6, (2, 4))
