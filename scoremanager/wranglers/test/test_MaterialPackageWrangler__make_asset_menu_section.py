# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageWrangler__make_asset_menu_section_01():
    r'''Behaves gracefully when no assets are found.
    '''

    input_ = 'blue~example~score m q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score Manager - scores',
        'Blue Example Score (2013)',
        'Blue Example Score (2013) - materials',
        ]
    assert score_manager._transcript.titles == titles


def test_MaterialPackageWrangler__make_asset_menu_section_02():
    r'''Omits score annotation inside score.
    '''

    input_ = 'red~example~score m q'
    score_manager._run(pending_input=input_)
    assert '(Red Example Score)' not in score_manager._transcript.contents


def test_MaterialPackageWrangler__make_asset_menu_section_03():
    r'''Includes score annotation outside of score.
    '''

    input_ = 'm q'
    score_manager._run(pending_input=input_)
    assert '(Red Example Score)' in score_manager._transcript.contents