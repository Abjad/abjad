# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageWrangler_go_to_next_score_01():

    input_ = 'red~example~score m >> q'
    score_manager._run(input_=input_)

    titles = [
        'Score Manager - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials',
        'Blue Example Score (2013)',
        ]
    assert score_manager._transcript.titles == titles


def test_MaterialPackageWrangler_go_to_next_score_02():

    input_ = 'm >> q'
    score_manager._run(input_=input_)

    titles = [
        'Score Manager - scores',
        'Score Manager - materials',
        'Blue Example Score (2013)',
        ]
    assert score_manager._transcript.titles == titles