# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_UserInputGetter_exec_01():

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='red~example~score score~setup instrumentation move exec 2**30 q')
    assert score_manager.session.io_transcript.signature == (12,)
