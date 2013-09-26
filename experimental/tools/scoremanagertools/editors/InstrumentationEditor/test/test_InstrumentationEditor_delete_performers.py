# -*- encoding: utf-8 -*-
from experimental import *


def test_InstrumentationEditor_delete_performers_01():
    r'''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(pending_user_input='red~example~score score~setup instrumentation rm q')
    assert score_manager.session.io_transcript.signature == (9,)

    score_manager._run(pending_user_input='red~example~score score~setup instrumentation rm b q')
    assert score_manager.session.io_transcript.signature == (11, (6, 9))

    score_manager._run(pending_user_input='red~example~score score~setup instrumentation rm home q')
    assert score_manager.session.io_transcript.signature == (11, (0, 9))

    score_manager._run(pending_user_input='red~example~score score~setup instrumentation rm score q')
    assert score_manager.session.io_transcript.signature == (11, (2, 9))

    score_manager._run(pending_user_input='red~example~score score~setup instrumentation rm foo q')
    assert score_manager.session.io_transcript.signature == (11, (6, 9))


def test_InstrumentationEditor_delete_performers_02():
    r'''Add three performers. Delete two.
    '''

    editor = scoremanagertools.editors.InstrumentationEditor()
    editor._run(pending_user_input='add acc default add bass default add bassoon default rm 3 rm 2 q')
    assert editor.target == scoretools.InstrumentationSpecifier(
        [scoretools.Performer('accordionist', instruments=[instrumenttools.Accordion()])])


def test_InstrumentationEditor_delete_performers_03():
    r'''Range handling.
    '''

    editor = scoremanagertools.editors.InstrumentationEditor()
    editor._run(pending_user_input='add 1-3 default default default rm 3-2 q')
    assert editor.target == scoretools.InstrumentationSpecifier(
        [scoretools.Performer('accordionist', instruments=[instrumenttools.Accordion()])])
