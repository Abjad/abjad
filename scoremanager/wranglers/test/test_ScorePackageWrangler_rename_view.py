# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageWrangler_rename_view_01():

    input_ = 'vnew _test_100 rm all'
    input_ += ' add Red~Example~Score done default q' 
    score_manager._run(pending_input=input_)
        
    input_ = 'vls q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents
    assert '_test_100' in contents
    assert '_test_101' not in contents

    input_ = 'vren _test_100 _test_101 default q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents

    input_ = 'vls q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents
    assert '_test_100' not in contents
    assert '_test_101' in contents

    input_ = 'vrm _test_101 default q'
    score_manager._run(pending_input=input_)

    input_ = 'vls q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents
    assert '_test_101' not in contents