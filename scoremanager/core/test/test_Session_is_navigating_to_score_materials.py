# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_Session_is_navigating_to_score_materials_01():
    r'''From build directory to materials directory.
    '''

    input_ = 'red~example~score u m q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build files',
        'Red Example Score (2013) - materials',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_materials_02():
    r'''From distribution directory to materials directory.
    '''

    input_ = 'red~example~score d m q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - distribution files',
        'Red Example Score (2013) - materials',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_materials_03():
    r'''From makers direcotry to materials directory.
    '''

    input_ = 'red~example~score k m q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - maker modules',
        'Red Example Score (2013) - materials',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_materials_04():
    r'''From materials directory to materials directory.
    '''

    input_ = 'red~example~score m m q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials',
        'Red Example Score (2013) - materials',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_materials_05():
    r'''From segments directory to materials directory.
    '''

    input_ = 'red~example~score g m q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments',
        'Red Example Score (2013) - materials',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_materials_06():
    r'''From setup menu to materials directory.
    '''

    input_ = 'red~example~score p m q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - setup',
        'Red Example Score (2013) - materials',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_score_materials_07():
    r'''From stylesheets menu to materials directory.
    '''

    input_ = 'red~example~score y m q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets',
        'Red Example Score (2013) - materials',
        ]
    assert score_manager._transcript.titles == titles