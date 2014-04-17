# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_StylesheetWrangler_remove_view_01():
    
    input_ = 'q'
    score_manager._run(pending_user_input=input_)