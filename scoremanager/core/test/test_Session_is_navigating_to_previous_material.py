# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Session_is_navigating_to_previous_material_01():
    r'''Previous material.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score m mtp mtp mtp mtp q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials',
        'Red Example Score (2013) - materials - tempo inventory',
        'Red Example Score (2013) - materials - pitch range inventory',
        'Red Example Score (2013) - materials - magic numbers',
        'Red Example Score (2013) - materials - tempo inventory',
        ]
    assert score_manager._transcript.titles == titles      
