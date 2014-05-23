# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_UserInputGetter_back_01():
    r'''Back works.
    '''

    input_ = 'red~example~score m tempo~inventory ae 1 d b q'
    score_manager._run(input_=input_)
    assert score_manager._transcript.signature == (16, (10, 13))