# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_Session_is_navigating_to_segment_library_01():
    r'''From build directory to segments directory.
    '''

    input_ = 'u g q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Score manager - build file library',
        'Score manager - segment library',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_segment_library_02():
    r'''From distribution directory to segments directory.
    '''

    input_ = 'd g q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Score manager - distribution artifact library',
        'Score manager - segment library',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_segment_library_03():
    r'''From makers directory to segments directory.
    '''

    input_ = 'k g q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Score manager - maker module library',
        'Score manager - segment library',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_segment_library_04():
    r'''From materials directory to segments directory.
    '''

    input_ = 'm g q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Score manager - material library',
        'Score manager - segment library',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_segment_library_05():
    r'''From segments directory to segments directory.
    '''

    input_ = 'g g q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Score manager - segment library',
        'Score manager - segment library',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_segment_library_06():
    r'''From stylesheets directory to segments directory.
    '''

    input_ = 'y g q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Score manager - stylesheet library',
        'Score manager - segment library',
        ]
    assert score_manager._transcript.titles == titles