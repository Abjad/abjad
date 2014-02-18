# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_UserInputGetter_home_01():

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score score~setup instrumentation move h q'
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (11, (0, 9))
