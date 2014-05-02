# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=False)


def test_ScorePackageWrangler_list_views_01():
    
    input_ = 'vls vnew _test rm all'
    input_ += ' add Red~Example~Score done default'
    input_ += ' vls vrm _test default vls q'
    score_manager._run(pending_user_input=input_)
    transcript = score_manager._transcript

    view_list_entries = [
        _ for _ in transcript
        if ('view found' in _.contents or 'views found' in _.contents)
        ]
    assert len(view_list_entries) == 3

    assert '_test' not in view_list_entries[0].contents
    assert '_test' in view_list_entries[1].contents
    assert '_test' not in view_list_entries[2].contents