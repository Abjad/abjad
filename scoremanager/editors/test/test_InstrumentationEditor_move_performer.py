# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_InstrumentationEditor_move_performer_01():
    r'''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score setup instrumentation move q'
    score_manager._run(pending_user_input=string)
    assert score_manager._session.transcript.signature == (9,)

    string = 'red~example~score setup instrumentation move b q'
    score_manager._run(pending_user_input=string)
    assert score_manager._session.transcript.signature == (11, (6, 9))

    string = 'red~example~score setup instrumentation move h q'
    score_manager._run(pending_user_input=string)
    assert score_manager._session.transcript.signature == (11, (0, 9))

    string = 'red~example~score setup instrumentation move s q'
    score_manager._run(pending_user_input=string)
    assert score_manager._session.transcript.signature == (11, (2, 9))

    string = 'red~example~score setup instrumentation move foo q'
    score_manager._run(pending_user_input=string)
    assert score_manager._session.transcript.signature == (11,)


def test_InstrumentationEditor_move_performer_02():
    r'''Add three performers. Make two moves.
    '''

    editor = scoremanager.editors.InstrumentationEditor()
    string = 'add accordionist default add bassist default'
    string += ' add bassoonist bassoon move 1 2 move 2 3 q'
    editor._run(pending_user_input=string)
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
