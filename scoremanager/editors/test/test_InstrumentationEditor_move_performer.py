# -*- encoding: utf-8 -*-
from experimental import *


def test_InstrumentationEditor_move_performer_01():
    r'''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='red~example~score score~setup instrumentation move q')
    assert score_manager.session.io_transcript.signature == (9,)

    score_manager._run(pending_user_input='red~example~score score~setup instrumentation move b q')
    assert score_manager.session.io_transcript.signature == (11, (6, 9))

    score_manager._run(pending_user_input='red~example~score score~setup instrumentation move home q')
    assert score_manager.session.io_transcript.signature == (11, (0, 9))

    score_manager._run(pending_user_input='red~example~score score~setup instrumentation move score q')
    assert score_manager.session.io_transcript.signature == (11, (2, 9))

    score_manager._run(pending_user_input='red~example~score score~setup instrumentation move foo q')
    assert score_manager.session.io_transcript.signature == (11,)


def test_InstrumentationEditor_move_performer_02():
    r'''Add three performers. Make two moves.
    '''

    editor = scoremanager.editors.InstrumentationEditor()
    editor._run(pending_user_input=
        'add accordionist default add bassist default add bassoonist bassoon move 1 2 move 2 3 q')
    assert editor.target == instrumenttools.InstrumentationSpecifier([
        instrumenttools.Performer(name='bassist', instruments=[instrumenttools.Contrabass()]),
        instrumenttools.Performer(name='bassoonist', instruments=[instrumenttools.Bassoon()]),
        instrumenttools.Performer(name='accordionist', instruments=[instrumenttools.Accordion()])])
