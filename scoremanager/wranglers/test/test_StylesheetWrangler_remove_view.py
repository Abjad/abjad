# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_StylesheetWrangler_remove_view_01():
    r'''Makes view. Removes view.
    '''

    input_ = 'y vnew _test rm all add clean-letter-14.ily done default q' 
    score_manager._run(pending_user_input=input_)

    input_ = 'y vls vrm _test default q'
    score_manager._run(pending_user_input=input_)
    contents = score_manager._transcript.contents
    assert 'view found:' in contents or 'views found:' in contents
    assert '_test' in contents

    input_ = 'y vls q'
    score_manager._run(pending_user_input=input_)
    contents = score_manager._transcript.contents
    assert 'view found:' in contents or 'views found:' in contents
    assert '_test' not in contents