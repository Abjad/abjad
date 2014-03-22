# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MakerModuleWrangler__make_asset_menu_section_01():
    r'''Behaves gracefully when no assets are found.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'blue~example~score k q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores', 
        'Blue Example Score (2013)',
        'Blue Example Score (2013) - makers',
        ]
    assert score_manager._transcript.titles == titles