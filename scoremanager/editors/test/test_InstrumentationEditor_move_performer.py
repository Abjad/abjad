# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_InstrumentationEditor_move_performer_01():
    r'''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score setup instrumentation mv q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (9,)

    input_ = 'red~example~score setup instrumentation mv b q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (11, (6, 9))

    input_ = 'red~example~score setup instrumentation mv h q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (11, (0, 9))

    input_ = 'red~example~score setup instrumentation mv s q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (11, (2, 9))

    input_ = 'red~example~score setup instrumentation mv foo q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (11,)


def test_InstrumentationEditor_move_performer_02():
    r'''Add three performers. Make two moves.
    '''

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.InstrumentationEditor(session=session)
    input_ = 'add accordionist default add bassist default'
    input_ += ' add bassoonist bassoon mv 1 2 mv 2 3 q'
    editor._run(pending_user_input=input_)
    assert editor.target == instrumenttools.InstrumentationSpecifier([
        instrumenttools.Performer(
            name='bassist', 
            instruments=[instrumenttools.Contrabass()],
            ),
        instrumenttools.Performer(
            name='bassoonist', 
            instruments=[instrumenttools.Bassoon()],
            ),
        instrumenttools.Performer(
            name='accordionist', 
            instruments=[instrumenttools.Accordion()],
            ),
        ])
