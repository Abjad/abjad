# -*- encoding: utf-8 -*-
import pytest
from experimental import *
from abjad.tools.instrumenttools import *


def test_PerformerEditor_move_instrument_01():
    r'''Quit, back, home, score & junk all work.
    '''
    pytest.skip('remove custom score name.')

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input="l'arch score~setup instrumentation flutist move q")
    assert score_manager.session.io_transcript.signature == (11,)

    score_manager._run(pending_user_input="l'arch score~setup instrumentation flutist move b q")
    assert score_manager.session.io_transcript.signature == (13, (8, 11))

    score_manager._run(pending_user_input="l'arch score~setup instrumentation flutist move home q")
    assert score_manager.session.io_transcript.signature == (13, (0, 11))

    score_manager._run(pending_user_input="l'arch score~setup instrumentation flutist move score q")
    assert score_manager.session.io_transcript.signature == (13, (2, 11))

    score_manager._run(pending_user_input="l'arch score~setup instrumentation flutist move foo q")
    assert score_manager.session.io_transcript.signature == (13,)


def test_PerformerEditor_move_instrument_02():
    r'''Add two instruments. Move them.
    '''

    editor = scoremanager.editors.PerformerEditor()
    editor._run(pending_user_input='add 1 add 2 move 1 2 q')
    assert editor.target == Performer(instruments=[AltoVoice(), Accordion()])
