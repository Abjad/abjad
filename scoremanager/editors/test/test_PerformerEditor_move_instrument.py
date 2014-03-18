# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_PerformerEditor_move_instrument_01():
    r'''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    string = 'étude~example~score setup instrumentation flutist mv q'
    score_manager._run(pending_user_input=string, is_test=True)
    assert score_manager._transcript.signature == (11,)

    string = 'étude~example~score setup instrumentation flutist mv b q'
    score_manager._run(pending_user_input=string, is_test=True)
    assert score_manager._transcript.signature == (13, (8, 11))

    string = 'étude~example~score setup instrumentation flutist mv h q'
    score_manager._run(pending_user_input=string, is_test=True)
    assert score_manager._transcript.signature == (13, (0, 11))

    string = 'étude~example~score setup instrumentation flutist mv s q'
    score_manager._run(pending_user_input=string, is_test=True)
    assert score_manager._transcript.signature == (13, (2, 11))

    string = 'étude~example~score setup instrumentation'
    string += ' flutist mv foo q'
    score_manager._run(pending_user_input=string, is_test=True)
    assert score_manager._transcript.signature == (13,)


def test_PerformerEditor_move_instrument_02():
    r'''Add two instruments. Move them.
    '''

    session = scoremanager.core.Session()
    editor = scoremanager.editors.PerformerEditor(session=session)
    editor._run(pending_user_input='add 1 add 2 mv 1 2 q')
    assert editor.target == instrumenttools.Performer(
        instruments=[
            instrumenttools.AltoVoice(), 
            instrumenttools.Accordion(),
            ],
        )
