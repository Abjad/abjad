# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_StylesheetWrangler_rename_view_01():
    r'''Works in library.
    '''

    input_ = 'y vnew _test_100 rm all add clean-letter-14.ily done default q' 
    score_manager._run(input_=input_)
        
    input_ = 'y vls q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents
    assert '_test_100' in contents
    assert '_test_101' not in contents

    input_ = 'y vren _test_100 _test_101 default q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    input_ = 'y vls q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents
    assert '_test_100' not in contents
    assert '_test_101' in contents

    input_ = 'y vrm _test_101 default q'
    score_manager._run(input_=input_)

    input_ = 'y vls q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents
    assert '_test_101' not in contents