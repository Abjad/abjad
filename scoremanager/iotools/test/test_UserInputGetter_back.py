# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_UserInputGetter_back_01():
    r'''Back works.
    '''

    input_ = 'red~example~score m tempo~inventory mae 1 d b q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (15, (10, 13))