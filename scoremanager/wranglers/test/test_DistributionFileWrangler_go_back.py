# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_DistributionFileWrangler_go_back_01():

    input_ = 'red~example~score d b q'
    score_manager._run(pending_input=input_)

    titles = [
        'Score manager - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - distribution files',
        'Red Example Score (2013)',
        ]
    assert score_manager._transcript.titles == titles


def test_DistributionFileWrangler_go_back_02():

    input_ = 'd b q'
    score_manager._run(pending_input=input_)

    titles = [
        'Score manager - scores',
        'Score manager - distribution files',
        'Score manager - scores',
        ]
    assert score_manager._transcript.titles == titles