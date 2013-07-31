# -*- encoding: utf-8 -*-
from abjad import *
from experimental import *


def test_PerformerEditor_name_01():
    r'''Quit, back and home all work.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(pending_user_input='red~example~score setup performers hornist name q')
    assert score_manager.session.io_transcript.signature == (11,)

    score_manager._run(pending_user_input='red~example~score setup performers hornist name b q')
    assert score_manager.session.io_transcript.signature == (13, (8, 11))

    score_manager._run(pending_user_input='red~example~score setup performers hornist name home q')
    assert score_manager.session.io_transcript.signature == (13, (0, 11))


def test_PerformerEditor_name_02():
    r'''String input only.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(pending_user_input='red~example~score setup performers hornist name -99 q')
    assert score_manager.session.io_transcript.signature == (13,)


def test_PerformerEditor_name_03():
    r'''Create, name and rename performer.
    '''

    editor = scoremanagertools.editors.PerformerEditor()
    editor._run(pending_user_input='name foo name bar q')
    assert editor.target == scoretools.Performer(name='bar')
