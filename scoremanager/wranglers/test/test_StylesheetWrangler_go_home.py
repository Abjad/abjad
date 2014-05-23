# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_StylesheetWrangler_go_home_01():

    input_ = 'red~example~score y h q'
    score_manager._run(input_=input_)

    titles = [
        'Score Manager - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets',
        'Score Manager - scores',
        ]
    assert score_manager._transcript.titles == titles


def test_StylesheetWrangler_go_home_02():

    input_ = 'y h q'
    score_manager._run(input_=input_)

    titles = [
        'Score Manager - scores',
        'Score Manager - stylesheets',
        'Score Manager - scores',
        ]
    assert score_manager._transcript.titles == titles