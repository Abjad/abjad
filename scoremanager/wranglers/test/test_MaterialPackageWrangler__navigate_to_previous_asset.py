# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialPackageWrangler__navigate_to_previous_asset_01():
    r'''Previous material.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score m << << << << q'
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