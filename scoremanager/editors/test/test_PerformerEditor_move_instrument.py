# -*- encoding: utf-8 -*-
import pytest
from abjad import *
from abjad.tools.instrumenttools import *
import scoremanager


def test_PerformerEditor_move_instrument_01():
    r'''Quit, back, home, score & junk all work.
    '''
    pytest.skip('remove custom score name.')

    score_manager = scoremanager.core.ScoreManager()
    string = "l'arch score~setup instrumentation flutist move q"
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (11,)

    string = "l'arch score~setup instrumentation flutist move b q"
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (13, (8, 11))

    string = "l'arch score~setup instrumentation flutist move h q"
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (13, (0, 11))

    string = "l'arch score~setup instrumentation flutist move s q"
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (13, (2, 11))

    string = "l'arch score~setup instrumentation flutist move foo q"
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (13,)


def test_PerformerEditor_move_instrument_02():
    r'''Add two instruments. Move them.
    '''

    editor = scoremanager.editors.PerformerEditor()
    editor._run(pending_user_input='add 1 add 2 move 1 2 q')
    assert editor.target == Performer(instruments=[AltoVoice(), Accordion()])
