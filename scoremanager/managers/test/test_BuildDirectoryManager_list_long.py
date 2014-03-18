# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_BuildDirectoryManager_list_long_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score u ll q'
    score_manager._run(pending_user_input=input_)
    transcript = score_manager._transcript

    assert transcript.entries[-2].lines[0].startswith('total')
    assert transcript.entries[-2].lines[1].startswith('-rw-r--r--')
