# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_BuildFileWrangler_go_to_current_score_01():

    input_ = 'red~example~score u s q'
    score_manager._run(pending_input=input_)

    titles = [
        'Score manager - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build files',
        'Red Example Score (2013)',
        ]
    assert score_manager._transcript.titles == titles


def test_BuildFileWrangler_go_to_current_score_02():

    input_ = 'u s q'
    score_manager._run(pending_input=input_)

    titles = [
        'Score manager - scores',
        'Score manager - build files',
        'Score manager - build files',
        ]
    assert score_manager._transcript.titles == titles