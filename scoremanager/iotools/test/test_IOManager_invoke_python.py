# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_IOManager_invoke_python_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'pyi 2**30 q'
    score_manager._run(pending_input=input_)

    assert '1073741824' in score_manager._transcript.contents