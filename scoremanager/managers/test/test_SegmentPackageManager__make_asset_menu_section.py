# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_SegmentPackageManager__make_asset_menu_section_01():
    r'''Behaves gracefully when no assets are found.
    '''

    score_manager = scoremanager.core.ScoreManager()
    input_ = 'blue~example~score g segment~01 q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Blue Example Score (2013)',
        'Blue Example Score (2013) - segments',
        'Blue Example Score (2013) - segments - segment 01',
        ]
    assert score_manager._transcript.titles == titles