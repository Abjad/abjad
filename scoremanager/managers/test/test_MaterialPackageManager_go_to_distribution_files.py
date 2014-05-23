# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageManager_go_to_distribution_files_01():

    input_ = 'red~example~score m tempo~inventory d q'
    score_manager._run(input_=input_)

    titles = [
        'Score Manager - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials',
        'Red Example Score (2013) - materials - tempo inventory (AE)',
        'Red Example Score (2013) - distribution files',
        ]
    assert score_manager._transcript.titles == titles