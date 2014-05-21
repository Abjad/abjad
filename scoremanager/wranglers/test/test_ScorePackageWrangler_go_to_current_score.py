# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageWrangler_go_to_current_score_01():
    r'''From materials directory to build directory.
    '''

    input_ = 's q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score manager - scores',
        'Score manager - scores',
        ]
    assert score_manager._transcript.titles == titles