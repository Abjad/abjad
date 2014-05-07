# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_DirectoryManager_invoke_shell_01():

    input_ = 'm example~numbers !pwd q'
    score_manager._run(pending_input=input_)
    pwd = score_manager._transcript.last_title
    assert os.path.sep in pwd