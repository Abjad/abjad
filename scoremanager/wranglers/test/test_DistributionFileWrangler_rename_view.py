# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_DistributionFileWrangler_rename_view_01():
    r'''Works in library.
    '''

    input_ = 'd vnew _test_100 rm all'
    input_ += ' add red-example-score.pdf~(Red~Example~Score) done <return> q' 
    score_manager._run(input_=input_)
        
    input_ = 'd vls q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents
    assert '_test_100' in contents
    assert '_test_101' not in contents

    input_ = 'd vren _test_100 _test_101 <return> q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    input_ = 'd vls q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents
    assert '_test_100' not in contents
    assert '_test_101' in contents

    input_ = 'd vrm _test_101 <return> q'
    score_manager._run(input_=input_)

    input_ = 'd vls q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents
    assert '_test_101' not in contents