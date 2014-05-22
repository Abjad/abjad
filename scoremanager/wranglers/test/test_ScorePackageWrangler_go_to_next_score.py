# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageWrangler_go_to_next_score_01():

    input_ = '>> >> q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score Manager - scores',
        'Blue Example Score (2013)',
        'Étude Example Score (2013)',
        ]
    assert score_manager._transcript.titles == titles