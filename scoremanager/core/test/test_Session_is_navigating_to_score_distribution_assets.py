# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_Session_is_navigating_to_score_distribution_assets_01():
    r'''From build directory to distribution directory.
    '''

    input_ = 'red~example~score u d q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build manager',
        'Red Example Score (2013) - distribution',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_distribution_assets_02():
    r'''From distribution directory to distribution directory.
    '''

    input_ = 'red~example~score d d q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - distribution',
        'Red Example Score (2013) - distribution',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_distribution_assets_03():
    r'''From makers directory to distribution directory.
    '''

    input_ = 'red~example~score k d q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - makers',
        'Red Example Score (2013) - distribution',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_distribution_assets_04():
    r'''From materials directory to distribution directory.
    '''

    input_ = 'red~example~score m d q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials',
        'Red Example Score (2013) - distribution',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_distribution_assets_05():
    r'''From segments directory to distribution directory.
    '''

    input_ = 'red~example~score g d q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments',
        'Red Example Score (2013) - distribution',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_distribution_assets_06():
    r'''From setup menu to distribution directory.
    '''

    input_ = 'red~example~score p d q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - setup',
        'Red Example Score (2013) - distribution',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_distribution_assets_07():
    r'''From stylesheets directory to distribution directory.
    '''

    input_ = 'red~example~score y d q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets',
        'Red Example Score (2013) - distribution',
        ]
    assert score_manager._transcript.titles == titles
