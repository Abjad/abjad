# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_Session_is_navigating_to_material_library_01():
    r'''From build file library to material library.
    '''

    input_ = 'u m q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Score manager - build files',
        'Score manager - materials',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_material_library_02():
    r'''From distribution file library to material library.
    '''

    input_ = 'd m q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Score manager - distribution files',
        'Score manager - materials',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_material_library_03():
    r'''From maker module library to material library.
    '''

    input_ = 'k m q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Score manager - maker modules',
        'Score manager - materials',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_material_library_04():
    r'''From material library to material library.
    '''

    input_ = 'm m q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Score manager - materials',
        'Score manager - materials',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_material_library_05():
    r'''From segment library to material library.
    '''

    input_ = 'g m q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Score manager - segments',
        'Score manager - materials',
        ]
    assert score_manager._transcript.titles == titles


def test_Session_is_navigating_to_material_library_06():
    r'''From stylesheets library to material library.
    '''

    input_ = 'y m q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Score manager - stylesheets',
        'Score manager - materials',
        ]
    assert score_manager._transcript.titles == titles