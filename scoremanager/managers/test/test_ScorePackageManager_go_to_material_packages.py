# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageManager_go_to_material_packages_01():

    input_ = 'red~example~score m q'
    score_manager._run(pending_input=input_)

    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials',
        ]
    assert score_manager._transcript.titles == titles