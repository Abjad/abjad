# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_ScorePackageManager_display_available_commands_01():
    
    input_ = 'red~example~score ? q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'Red Example Score (2013) - available commands' in contents