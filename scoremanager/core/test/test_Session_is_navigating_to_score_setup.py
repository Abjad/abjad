# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_Session_is_navigating_to_score_setup_01():
    r'''From build directory to score setup.
    '''

    input_ = 'red~example~score u p q'
    score_manager._run(pending_user_input=input_, is_test=True)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build manager',
        'Red Example Score (2013) - setup',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_setup_02():
    r'''From distribution directory to score setup.
    '''

    input_ = 'red~example~score d p q'
    score_manager._run(pending_user_input=input_, is_test=True)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - distribution',
        'Red Example Score (2013) - setup',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_setup_03():
    r'''From makers directory to score setup.
    '''

    input_ = 'red~example~score k p q'
    score_manager._run(pending_user_input=input_, is_test=True)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - makers',
        'Red Example Score (2013) - setup',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_setup_04():
    r'''From materials directory to score setup.
    '''

    input_ = 'red~example~score m p q'
    score_manager._run(pending_user_input=input_, is_test=True)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials',
        'Red Example Score (2013) - setup',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_setup_05():
    r'''From segments directory to score setup.
    '''

    input_ = 'red~example~score g p q'
    score_manager._run(pending_user_input=input_, is_test=True)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments',
        'Red Example Score (2013) - setup',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_setup_06():
    r'''From setup menu to score setup.
    '''

    input_ = 'red~example~score p p q'
    score_manager._run(pending_user_input=input_, is_test=True)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - setup',
        'Red Example Score (2013) - setup',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_setup_07():
    r'''From stylesheets directory to score setup.
    '''

    input_ = 'red~example~score y p q'
    score_manager._run(pending_user_input=input_, is_test=True)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets',
        'Red Example Score (2013) - setup',
        ]
    assert score_manager._transcript.titles == titles
