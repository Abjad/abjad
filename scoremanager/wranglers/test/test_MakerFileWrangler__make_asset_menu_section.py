# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MakerFileWrangler__make_asset_menu_section_01():
    r'''Behaves gracefully when no assets are found.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'blue~example~score k q'
    score_manager._run(input_=input_)
    titles = [
        'Score Manager - scores',
        'Blue Example Score (2013)',
        'Blue Example Score (2013) - maker files',
        ]
    assert score_manager._transcript.titles == titles