# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_Session_is_navigating_to_score_makers_01():
    r'''From build directory to makers directory.
    '''

    input_ = 'red~example~score u k q'
    score_manager._run(pending_user_input=input_, is_test=True)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build manager',
        'Red Example Score (2013) - makers',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_makers_02():
    r'''From distribution directory to makers directory.
    '''

    input_ = 'red~example~score d k q'
    score_manager._run(pending_user_input=input_, is_test=True)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - distribution',
        'Red Example Score (2013) - makers',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_makers_03():
    r'''From makers directory to makers directory.
    '''

    input_ = 'red~example~score k k q'
    score_manager._run(pending_user_input=input_, is_test=True)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - makers',
        'Red Example Score (2013) - makers',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_makers_04():
    r'''From materials directory to makers directory.
    '''

    input_ = 'red~example~score m k q'
    score_manager._run(pending_user_input=input_, is_test=True)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials',
        'Red Example Score (2013) - makers',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_makers_05():
    r'''From segments directory to makers directory.
    '''

    input_ = 'red~example~score g k q'
    score_manager._run(pending_user_input=input_, is_test=True)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments',
        'Red Example Score (2013) - makers',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_makers_06():
    r'''From setup menu to makers directory.
    '''

    input_ = 'red~example~score p k q'
    score_manager._run(pending_user_input=input_, is_test=True)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - setup',
        'Red Example Score (2013) - makers',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_makers_07():
    r'''From stylesheets menu to makers directory.
    '''

    input_ = 'red~example~score y k q'
    score_manager._run(pending_user_input=input_, is_test=True)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets',
        'Red Example Score (2013) - makers',
        ]
    assert score_manager._transcript.titles == titles
