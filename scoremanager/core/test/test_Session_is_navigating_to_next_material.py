# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Session_is_navigating_to_next_material_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score m >> >> >> >> q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials',
        'Red Example Score (2013) - materials - magic numbers',
        'Red Example Score (2013) - materials - pitch range inventory',
        'Red Example Score (2013) - materials - tempo inventory',
        'Red Example Score (2013) - materials - magic numbers',
        ]
    assert score_manager._transcript.titles == titles      