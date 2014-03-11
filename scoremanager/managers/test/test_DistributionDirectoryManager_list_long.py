# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_DistributionDirectoryManager_list_long_01():

    score_manager = scoremanager.core.ScoreManager()
    input_ = 'red~example~score d ll q'
    score_manager._run(pending_user_input=input_, is_test=True)
    transcript = score_manager._transcript

    assert transcript.entries[-2].lines == ['']
