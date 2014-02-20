# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_UserInputGetter_exec_01():

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score setup instrumentation move pyi 2**30 q'
    score_manager._run(pending_user_input=string)
    assert score_manager._session.io_transcript.signature == (12,)
