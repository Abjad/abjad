# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScoreManager_repository_status_01():
    r'''Works with all scores.
    '''

    input_ = 'ssl rst default q'
    score_manager._run(pending_user_input=input_)
    titles = score_manager._transcript.titles

    assert titles[-2] == 'Press return to continue.'
    assert titles[-1] == 'Score manager - all scores'


def test_ScoreManager_repository_status_02():
    r'''Works with active scores.
    '''

    input_ = 'ssv rst default q'
    score_manager._run(pending_user_input=input_)
    titles = score_manager._transcript.titles

    assert titles[-2] == 'Press return to continue.'
    assert titles[-1] == 'Score manager - active scores'


def test_ScoreManager_repository_status_03():
    r'''Works with example scores.
    '''

    input_ = 'ssx rst default q'
    score_manager._run(pending_user_input=input_)
    titles = score_manager._transcript.titles

    assert titles[-2] == 'Press return to continue.'
    assert titles[-1] == 'Score manager - example scores'