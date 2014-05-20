# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageManager_display_available_commands_01():
    
    input_ = 'red~example~score g A ? q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents

    assert 'segments - A - available commands' in contents