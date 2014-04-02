# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_UserInputGetter_exec_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score p instr ps mv pyi 2**30 q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (14,)