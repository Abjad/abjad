# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_UserInputGetter_score_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score m tempo~inventory ae 1 d s q'
    score_manager._run(input_=input_)
    assert score_manager._transcript.signature == (16, (2, 13))