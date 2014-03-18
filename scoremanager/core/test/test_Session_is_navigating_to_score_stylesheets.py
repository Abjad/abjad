# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_Session_is_navigating_to_score_stylesheets_01():
    r'''From build directory to stylesheets directory.
    '''

    input_ = 'red~example~score u y q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build manager',
        'Red Example Score (2013) - stylesheets',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_stylesheets_02():
    r'''From distribution directory to stylesheets directory.
    '''

    input_ = 'red~example~score d y q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - distribution',
        'Red Example Score (2013) - stylesheets',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_stylesheets_03():
    r'''From makers directory to stylesheets directory.
    '''

    input_ = 'red~example~score k y q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - makers',
        'Red Example Score (2013) - stylesheets',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_stylesheets_04():
    r'''From materials directory to stylesheets directory.
    '''

    input_ = 'red~example~score m y q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials',
        'Red Example Score (2013) - stylesheets',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_stylesheets_05():
    r'''From segments directory to stylesheets directory.
    '''

    input_ = 'red~example~score g y q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments',
        'Red Example Score (2013) - stylesheets',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_stylesheets_06():
    r'''From setup menu to stylesheets directory.
    '''

    input_ = 'red~example~score p y q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - setup',
        'Red Example Score (2013) - stylesheets',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_stylesheets_07():
    r'''From stylesheets directory to stylesheets directory.
    '''

    input_ = 'red~example~score y y q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets',
        'Red Example Score (2013) - stylesheets',
        ]
    assert score_manager._transcript.titles == titles
