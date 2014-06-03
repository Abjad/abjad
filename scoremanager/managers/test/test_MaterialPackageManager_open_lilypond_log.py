# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.AbjadIDE(is_test=True)


def test_MaterialPackageManager_open_lilypond_log_01():

    input_ = 'red~example~score m tempo~inventory log q'
    score_manager._run(input_=input_)
    
    assert score_manager._session._attempted_to_open_file