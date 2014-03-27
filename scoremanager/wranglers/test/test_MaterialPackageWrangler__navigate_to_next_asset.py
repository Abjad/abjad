# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialPackageWrangler__navigate_to_next_asset_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score m > > > > q'
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


def test_MaterialPackageWrangler__navigate_to_next_asset_02():
    r'''State is maintained cleanly moving between different types of sibling
    asset.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score m > > g > > q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials',
        'Red Example Score (2013) - materials - magic numbers',
        'Red Example Score (2013) - materials - pitch range inventory',
        'Red Example Score (2013) - segments',
        'Red Example Score (2013) - segments - segment 01',
        'Red Example Score (2013) - segments - segment 02',
        ]
    assert score_manager._transcript.titles == titles      