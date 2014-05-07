# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MakerModuleWrangler_rename_view_01():
    r'''Works in library.
    '''

    input_ = 'k vnew _test_100 rm all'
    input_ += ' add RedExampleScoreTemplate.py~(Red~Example~Score)'
    input_ += ' done default q' 
    score_manager._run(pending_input=input_)
        
    input_ = 'k vls q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents
    assert '_test_100' in contents
    assert '_test_101' not in contents

    input_ = 'k vren _test_100 _test_101 default q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents

    input_ = 'k vls q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents
    assert '_test_100' not in contents
    assert '_test_101' in contents

    input_ = 'k vrm _test_101 default q'
    score_manager._run(pending_input=input_)

    input_ = 'k vls q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents
    assert '_test_101' not in contents