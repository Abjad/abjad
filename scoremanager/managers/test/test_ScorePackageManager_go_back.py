# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageManager_go_back_01():

    input_ = 'red~example~score b q'
    score_manager._run(input_=input_)

    titles = [
        'Score Manager - scores',
        'Red Example Score (2013)',
        'Score Manager - scores',
        ]
    assert score_manager._transcript.titles == titles