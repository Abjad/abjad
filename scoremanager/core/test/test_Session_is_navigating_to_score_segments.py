# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager()


def test_Session_is_navigating_to_score_segments_01():
    r'''From build directory to segments directory.
    '''

    input_ = 'red~example~score u g q'
    score_manager._run(pending_user_input=input_, is_test=True)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build manager',
        'Red Example Score (2013) - segments',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_segments_02():
    r'''From distribution directory to segments directory.
    '''

    input_ = 'red~example~score d g q'
    score_manager._run(pending_user_input=input_, is_test=True)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - distribution',
        'Red Example Score (2013) - segments',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_segments_03():
    r'''From makers directory to segments directory.
    '''
    pytest.skip('active makers and then unskip.')

    input_ = 'red~example~score k g q'
    score_manager._run(pending_user_input=input_, is_test=True)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - makers',
        'Red Example Score (2013) - segments',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_segments_04():
    r'''From materials directory to segments directory.
    '''

    input_ = 'red~example~score m g q'
    score_manager._run(pending_user_input=input_, is_test=True)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials',
        'Red Example Score (2013) - segments',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_segments_05():
    r'''From segments directory to segments directory.
    '''

    input_ = 'red~example~score g g q'
    score_manager._run(pending_user_input=input_, is_test=True)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments',
        'Red Example Score (2013) - segments',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_segments_06():
    r'''From setup menu to segments directory.
    '''

    input_ = 'red~example~score p g q'
    score_manager._run(pending_user_input=input_, is_test=True)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - setup',
        'Red Example Score (2013) - segments',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_segments_07():
    r'''From stylesheets directory to segments directory.
    '''

    input_ = 'red~example~score y g q'
    score_manager._run(pending_user_input=input_, is_test=True)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets',
        'Red Example Score (2013) - segments',
        ]
    assert score_manager._transcript.titles == titles
