# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_StylesheetWrangler_go_to_current_score_01():

    input_ = 'red~example~score y s q'
    score_manager._run(input_=input_)

    titles = [
        'Score Manager - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets',
        'Red Example Score (2013)',
        ]
    assert score_manager._transcript.titles == titles


def test_StylesheetWrangler_go_to_current_score_02():

    input_ = 'y s q'
    score_manager._run(input_=input_)

    titles = [
        'Score Manager - scores',
        'Score Manager - stylesheets',
        'Score Manager - stylesheets',
        ]
    assert score_manager._transcript.titles == titles