# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageWrangler_invoke_shell_01():

    input_ = '!pwd q'
    score_manager._run(pending_user_input=input_)
    pwd = score_manager._transcript.last_title
    assert os.path.sep in pwd