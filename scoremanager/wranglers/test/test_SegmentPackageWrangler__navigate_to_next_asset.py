# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_SegmentPackageWrangler__navigate_to_next_asset_01():
    r'''Previous material package.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score g > > > > q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments',
        'Red Example Score (2013) - segments - segment 01',
        'Red Example Score (2013) - segments - segment 02',
        'Red Example Score (2013) - segments - segment 03',
        'Red Example Score (2013) - segments - segment 01',
        ]
    assert score_manager._transcript.titles == titles      