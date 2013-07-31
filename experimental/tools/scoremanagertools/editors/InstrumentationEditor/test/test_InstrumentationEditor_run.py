# -*- encoding: utf-8 -*-
from experimental import *


def test_InstrumentationEditor_run_01():
    r'''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(pending_user_input='red~example~score setup perf q')
    assert score_manager.session.io_transcript.signature == (8,)

    score_manager._run(pending_user_input='red~example~score setup perf b q')
    assert score_manager.session.io_transcript.signature == (10, (4, 8))

    score_manager._run(pending_user_input='red~example~score setup perf home q')
    assert score_manager.session.io_transcript.signature == (10, (0, 8))

    score_manager._run(pending_user_input='red~example~score setup perf score q')
    assert score_manager.session.io_transcript.signature == (10, (2, 8))

    score_manager._run(pending_user_input='red~example~score setup perf foo q')
    assert score_manager.session.io_transcript.signature == (10, (6, 8))
