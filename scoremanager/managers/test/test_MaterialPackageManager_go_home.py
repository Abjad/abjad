# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageManager_go_home_01():

    input_ = 'red~example~score m tempo~inventory h q'
    score_manager._run(pending_input=input_)

    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials',
        'Red Example Score (2013) - materials - tempo inventory (AE)',
        'Score manager - example scores',
        ]
    assert score_manager._transcript.titles == titles